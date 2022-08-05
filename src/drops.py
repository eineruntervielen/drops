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


class Drops:
    default_config = MappingProxyType(dict(
        name=__name__,
    ))

    def __init__(self, maxsize: int = 0) -> None:
        self.event_queue: EventQueue = EventQueue(maxsize=maxsize)

    def _register_messages(self, messages: list[DropsMessage]):
        ...

    def _register_queue_members(self, members: list[Member]):
        ...

    def engine():
        ...


class EventQueue(PriorityQueue):
    maxsize: int = 0

    def __init__(self, messages: list[DropsMessage], maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.channels = {msg: [] for msg in messages}


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


class Member:
    counter = count()

    def __init__(self, name: str):
        self.member_id: int = next(self.counter)
        self.name = name

    def update(self):
        pass

