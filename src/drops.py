from __future__ import annotations

import datetime as dt

from itertools import count
from typing import Any, Optional
from queue import PriorityQueue
from enum import Enum, unique


# Typing
Datetime: dt.datetime


@unique
class DropsMessage(Enum):
    ...


class ChannelOptions:
    filter_am_i_receiver: bool = True
    filter_am_i_sender: bool = True


class Drops:

    def __init__(self,
                 messages: DropsMessage,
                 members: Member
                 ) -> None:
        self.messages: DropsMessage = messages
        self._register_messages(messages=messages)
        self._register_members(members=members)

    def _register_messages(self, messages: list[DropsMessage]):
        self.event_queue: EventQueue = EventQueue(messages=messages)

    def _register_members(self, members: list[Member]):
        self.members = members
        for name, member_class in self.members.items():
            m = member_class.value(name=name, event_queue=self.event_queue)

    def run(self):
        while self.event_queue:
            event = self.event_queue.queue.get()
            for member in self.event_queue.channels[event.message]:
                member.update(event=event)


class Event:
    counter = count()

    def __init__(self, *, time: Datetime, message: DropsMessage, sender: Member = None, receiver: Optional[Member] | Optional[list[Member]] = None, ** kwargs) -> None:
        self.event_id: int = next(self.counter)
        self.time: Datetime = time
        self.message: DropsMessage = message
        self.sender: Any = sender
        self.receiver: Any = receiver
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'Event(id={self.id}, time={self.time}, message={self.message})'

    def __lt__(self, __o: object) -> bool:
        return self.time < __o.time and self.event_id < __o.event_id


class EventQueue(PriorityQueue):
    maxsize: int = 0

    def __init__(self, messages: list[DropsMessage], maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.queue: PriorityQueue = PriorityQueue()
        self.channels = {msg: [] for msg in messages}


class Member:
    counter = count()

    def __init__(self, name: str, event_queue: EventQueue):
        self.member_id: int = next(self.counter)
        self.name = name
        self._event_queue: EventQueue = event_queue
        self._register()
        for channel in self.default_config['channels']:
            if not hasattr(self, channel.value):
                raise NotImplementedError(f'Member {self} needs to implement a callback for channel {channel}')

    def _register(self):
        for channel in self.default_config['channels']:
            self._event_queue.channels[channel].append(self)

    def update(self, event: Event):
        """Every member is updated according to its subscriptions to
        the channels on the EventQueue. If an Event occurs the member
        receives an update on which a pseudo-callback function
        is called.

        Args:
            event (Event): Event to trigger the pseudo-callback
        """
        getattr(self, event.message.value)(event)

    def share(self, *, time: Datetime, message: DropsMessage, **kwargs):
        """Inserts an upcoming Event into the EventQueue.

        Args:
            time (Datetime): Future point in time when the event happens
            message (DropsMessage): Message that carries the informations
        """
        self._event_queue.queue.put(
            Event(time=time, message=message, sender=self, kwargs=kwargs)
        )
