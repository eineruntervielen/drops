from __future__ import annotations

import datetime as dt

from itertools import count
from queue import PriorityQueue
from enum import Enum, unique
from tempfile import gettempdir
from types import MappingProxyType


# Typing
Datetime: dt.datetime


@unique
class DropsMessage(Enum):
    ...


class ChannelFilters:
    filter_am_i_receiver: boolean = True
    filter_am_i_sender: boolean = True


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
        self.members: Member = members
        for member in self.members:
            member._register

    def run(self):
        while self.event_queue:
            event = self.event_queue.queue.get()
            for member in self.event_queue.channels[event.message]:
                member.update(event=event)


class Event:
    counter = count()

    def __init__(self, *, time: Datetime, message: DropsMessage, **kwargs) -> None:
        self.event_id: int = next(self.counter)
        self.time: Datetime = time
        self.message: DropsMessage = message
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return f'Event(id={self.id}, time={self.time}, message={self.message})'


class EventQueue(PriorityQueue):
    maxsize: int = 0

    def __init__(self, messages: list[DropsMessage], maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.queue: PriorityQueue = PriorityQueue()
        self.channels = {msg: [] for msg in messages}


class Member:
    counter = count()

    def __init__(self, name: str, queue: EventQueue):
        self.member_id: int = next(self.counter)
        self.name = name
        self.queue: EventQueue = queue
        self._register()

    def _register(self):
        for channel in self.channels:
            self.queue.channels[channel].append(self)

    def update(self, event: Event):
        getattr(self, event.message.value)(event)
