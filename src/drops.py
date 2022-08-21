from __future__ import annotations

import sys
import importlib.util
import datetime as dt

from dataclasses import dataclass
from enum import Enum, unique
from itertools import count
from pathlib import Path
from queue import PriorityQueue
from types import MappingProxyType
from typing import Any, Optional

# Typing
Datetime: dt.datetime


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
class ChannelOptions:
    filter_am_i_receiver: Optional[bool] = True
    filter_am_i_sender: Optional[bool] = True


class Drops:
    default_config = MappingProxyType(
        {
            'MAXSIZE': -1,
        }
    )

    def __init__(self,
                 end,
                 messages: DropsMessage,  # todo maybe both ways?
                 members: Member,  # todo maybe both ways?
                 scenario_path: Path = None,
                 maxsize: int = default_config['MAXSIZE'],
                 ) -> None:
        self.maxsize = maxsize
        self.end = end
        self.scenario_path = scenario_path
        if self.scenario_path:
            self.__load_modules()
        else:
            self.messages = messages
            self.members = members
        self.__register_messages()
        self.__register_members()

    def __load_modules(self):
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

    def __register_messages(self):
        # todo because self.messages is not the class enum by itself we need to call messages.name everywhere
        # this sucks
        self.event_queue: EventQueue = EventQueue(
            messages=self.messages, maxsize=self.maxsize)

    def __register_members(self):
        for member in self.members:
            member.value(name=member, event_queue=self.event_queue)

    def run(self):
        while not self.event_queue.empty():
            event = self.event_queue.get(block=False)
            if event.time <= self.end:
                for member in self.event_queue.channels[event.message.name]:
                    member.update(event=event)
            else:
                break


class EventState(Enum):
    OPEN = 'open'
    PROCESSED = 'processed'


class Event:
    counter = count()

    def __init__(self, *, time: Datetime | int, message: DropsMessage, sender: Member = None,
                 receiver: Optional[Member] | Optional[list[Member]] = None, **kwargs) -> None:
        self.event_id: int = next(self.counter)
        self.time: Datetime | int = time
        self.message: DropsMessage = message
        self.sender: Any = sender
        self.receiver: Any = receiver
        self.state: EventState = EventState.OPEN
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'Event(id={self.id}, time={self.time}, message={self.message})'

    def __lt__(self, __o: object) -> bool:
        return self.time < __o.time and self.event_id < __o.event_id


class EventQueue(PriorityQueue):
    maxsize: int = 0

    def __init__(self, messages, maxsize):
        super().__init__(maxsize)
        self.channels = {msg.name: [] for msg in messages}


class Member:
    counter = count()
    subscriptions: dict[DropsMessage, ChannelOptions] = {}

    def __init__(self, name: str, event_queue: EventQueue):
        self.member_id: int = next(self.counter)
        self.name = name
        self._event_queue: EventQueue = event_queue
        self.__check_subscriptions()
        self.__register()
        self.__check_subcallbacks()

    def __check_subscriptions(self):
        if not self.subscriptions:
            # raise NotImplementedError(
            print(NotImplementedError(
                f'The Member {self.name} has no subscriptions. Are you shure thats intended?'
            ))

    def __register(self):
        for sub in self.subscriptions:
            self._event_queue.channels[sub.name].append(self)

    def __check_subcallbacks(self):
        for sub in self.subscriptions:
            reaction_name: str = '_' + str(sub.name).lower()
            if not hasattr(self, reaction_name):
                raise NotImplementedError(
                    f'Member {self} needs to implement a reaction for channel {sub}'
                )

    def update(self, event: Event):
        """Every member is updated according to its subscriptions to
        the channels on the EventQueue. If an Event occurs the member
        receives an update on which a pseudo-callback function
        is called.

        Args:
            event (Event): Event to trigger the pseudo-callback
        """
        getattr(self, '_' + event.message.name.lower())(event)

    def share(self, *, time: Datetime | int, message: DropsMessage, **kwargs):
        """Inserts an upcoming Event into the EventQueue.

        Args:
            time (Datetime): Future point in time when the event happens
            message (DropsMessage): Message that carries the information
        """
        self._event_queue.put(
            Event(time=time, message=message, sender=self, kwargs=kwargs)
        )
