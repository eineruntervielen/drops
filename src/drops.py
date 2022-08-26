from __future__ import annotations

import sys
import importlib.util
import datetime as dt
import threading

from dataclasses import dataclass
from enum import Enum, unique
from http.server import SimpleHTTPRequestHandler, HTTPServer
from itertools import count
from pathlib import Path
from queue import PriorityQueue
from types import MappingProxyType
from typing import Optional

# Typing
Datetime: dt.datetime
DropsTime: dt.datetime | dt.time | int


@unique
class DropsMessage(Enum):
    """An implementation of a dx-centered Enum.
    Since DropsMessage's pseudo-callbacks are by design the lowercase
    of the DropsMessage name, the value of the enum is of no interest.
    Therefore, one can use it like this:

    class Messages(DropsMessage):
        HELLO = ()
        GOOD_BY = ()
        HOW_ARE_YOU = ()
    """

    def __new__(cls):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__) + 1
        return obj

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}>'


@dataclass
class MessageFilter:
    """Used to filter out messages that are none of the DropsComponent's
    business. Maybe there exists a Message.HELLO and the component
    is only reacting if the greeting is directed to itself and not a
    general greeting.
    """
    filter_am_i_receiver: Optional[bool] = False
    filter_am_i_sender: Optional[bool] = False


class DropsHTTPRequestHandler(SimpleHTTPRequestHandler):
    record_provider: any

    def do_GET(self):
        if self.path == '/':
            try:
                self.send_response(200)
            except:
                self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(f'{DropsHTTPRequestHandler.record_provider}', 'utf-8'))


class Drops:
    default_config = MappingProxyType(
        {
            'MAXSIZE': -1,
            'END': None
        }
    )

    def __init__(self,
                 messages,  # TODO typing
                 members,  # TODO typing
                 scenario_path: Path = None,
                 maxsize: int = default_config['MAXSIZE'],
                 end=default_config['END'],
                 ) -> None:
        self.maxsize = maxsize
        self.end = end
        self.scenario_path = scenario_path
        if self.scenario_path:
            self._load_modules()
        else:
            self.messages = messages
            self.members = members
        self._register_messages()
        self._register_members()

    def __str__(self):
        return f'Drops Application\n' \
               f'scenario={self.scenario_path}\n' \
               f'members={self.messages}'

    def _load_modules(self):
        # todo this needs to be understood in greater detail but looks awesome
        spec_members = importlib.util.spec_from_file_location(
            "members", self.scenario_path / 'model/members.py')
        spec_messages = importlib.util.spec_from_file_location(
            "messages", self.scenario_path / 'model/messages.py')
        members = importlib.util.module_from_spec(spec_members)
        messages = importlib.util.module_from_spec(spec_messages)
        sys.modules["members"] = members
        sys.modules["messages"] = messages
        spec_members.loader.exec_module(members)
        spec_messages.loader.exec_module(messages)
        self.members = members.Members
        self.messages = messages.Messages

    def _register_messages(self):
        self.event_queue: EventQueue = EventQueue(
            messages=self.messages,
            maxsize=self.maxsize
        )

    def _register_members(self):
        for name, member in self.members.items():
            member(name=name, event_queue=self.event_queue)

    def run(self):
        while not self.event_queue.empty():
            event = self.event_queue.get(block=False)
            if self.end:
                if event.time <= self.end:
                    for member in self.event_queue.channels[event.msg.name]:
                        # TODO: check if member has filters
                        member.inform(event=event)
                else:
                    break
            else:
                for member in self.event_queue.channels[event.message.name]:
                    member.inform(event=event)

    def serve(self, host: str, port: int):
        DropsHTTPRequestHandler.record_provider = self
        httpd = HTTPServer((host, port), DropsHTTPRequestHandler)
        thread = threading.Thread(target=self.run)
        try:
            thread.start()
            httpd.serve_forever()
        except KeyboardInterrupt as kbd:
            print(kbd)


class Event:
    counter = count()

    def __init__(self, *, time: DropsTime, msg: DropsMessage, sender: DropsComponent = None,
                 receiver: Optional[DropsComponent] | Optional[list[DropsComponent]] = None, **kwargs) -> None:
        self.event_id: int = next(self.counter)
        self.time: DropsTime = time
        self.msg: DropsMessage = msg
        self.sender: DropsComponent = sender
        self.receiver: DropsComponent = receiver
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'Event(id={self.event_id}, time={self.time}, message={self.msg})'

    def __lt__(self, __o: object) -> bool:
        return self.time < __o.time and self.event_id < __o.event_id


class EventQueue(PriorityQueue):
    maxsize: int = 0

    def __init__(self, messages, maxsize):
        super().__init__(maxsize)
        self.channels = {msg.name: [] for msg in messages}


class DropsComponent:
    counter = count()
    subscriptions: dict[DropsMessage, MessageFilter] = {}

    def __init__(self, name: str, event_queue: EventQueue):
        self.component_id: int = next(self.counter)
        self.name: str = name
        self._event_queue: EventQueue = event_queue

        self._check_subscriptions()
        self._subscribe()
        self._check_reactions()

    def _check_subscriptions(self):
        if not self.subscriptions:
            print(NotImplementedError(
                f'The component {self.name} has no subscriptions. Are you shure that was intended?'
            ))

    def _subscribe(self):
        for subscription in self.subscriptions:
            self._event_queue.channels[subscription.name].append(self)

    def _check_reactions(self):
        for subscription in self.subscriptions:
            reaction_name: str = str(subscription.name).lower()
            if not hasattr(self, reaction_name):
                raise NotImplementedError(
                    f'Member {self} needs to implement a reaction for the subscription {subscription}'
                )

    def inform(self, event: Event):
        """Every component is informed according to its subscriptions to
        the channels on the EventQueue. If an Event occurs the component
        receives an information on which a reaction-method is emitted.

        Args:
            event (Event): Event to trigger the reaction-method
        """
        getattr(self, event.msg.name.lower())(event)

    def share(self, *, time: Datetime | int, msg: DropsMessage, **kwargs):
        """Inserts an upcoming Event into the EventQueue.

        Args:
            time (Datetime): Future point in time when the event happens
            msg: (DropsMessage): Message that carries the information
            **kwargs: The rest of the attributes to create an event
        """
        sargs = locals()
        self._event_queue.put(
            Event(time=time, msg=msg, sender=self, **sargs['kwargs'])
        )
