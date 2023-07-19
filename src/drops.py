from __future__ import annotations

import inspect
from itertools import count
from queue import PriorityQueue
from typing import Any, Callable, Hashable, Iterable, MutableMapping, NamedTuple

AnyDict = dict[str, Any]


class DelayedEvent(NamedTuple):
    msg: Hashable
    delay: int
    payload: AnyDict = {}


class ScheduledEvent(NamedTuple):
    msg: Hashable
    time: int
    payload: AnyDict


class Event:
    counter = count()

    def __init__(self, *, msg, time, sender: str = "",
                 payload: AnyDict | None):
        self.event_id: int = next(self.counter)
        self.msg = msg
        self.time = time
        self.sender = sender
        self.payload = payload if payload else {}

    def __getattr__(self, item: Any) -> Any:
        return item

    def __str__(self):
        return f'Event(id={self.event_id}, message={self.msg}, time={self.time}, payload={self.payload})'

    def __lt__(self, other):
        return self.time < other.time or self.time == other.time and self.event_id < other.event_id


EventCallback = Callable[[Event], DelayedEvent | ScheduledEvent | None]


class EventQueue(PriorityQueue):

    def __init__(self, maxsize):
        super().__init__(maxsize)
        self.channels: MutableMapping[Hashable, list[Callable]] = {}

    def open_new_channel(self, msg: Hashable):
        if not self.channels.get(msg):
            self.channels[msg] = []


class Drops:
    maxsize = -1
    END: None

    def __init__(self, name: str, end) -> None:
        self.name = name
        self.end = end if end else self.END
        self.event_queue = EventQueue(maxsize=self.maxsize)
        self.now = 0

    def register_callback(self, func: Callable[[Event], Event], msgs: Iterable[Hashable]):
        for msg in msgs:
            self.event_queue.open_new_channel(msg)
            self.event_queue.channels[msg].append(func)

    def register_class(self, cls, **kwargs):
        inst = cls(**kwargs)
        for msg in inst.consumptions:
            self.event_queue.open_new_channel(msg)
            self.event_queue.channels[msg].append(inst)

    @staticmethod
    def call_member(member, event: Event):
        if inspect.isfunction(member):
            follow_up = member(event)
            return follow_up
        else:
            follow_up = getattr(member, str(event.msg))(event)
            return follow_up

    def create_follow_up_event(self, pre_event: DelayedEvent | ScheduledEvent) -> Event:
        match pre_event:
            case DelayedEvent():
                time = self.now + pre_event.delay
                return Event(msg=pre_event.msg, time=time, payload=pre_event.payload)
            case ScheduledEvent():
                time = pre_event.time
                return Event(msg=pre_event.msg, time=time, payload=pre_event.payload)

    def inform_all(self, event):
        for member in self.event_queue.channels[event.msg]:
            if follow_up := self.call_member(member, event):
                new_event = self.create_follow_up_event(follow_up)
                self.event_queue.put(new_event)

    def run(self):
        while not self.event_queue.empty():
            event = self.event_queue.get(block=False)
            self.now = event.time
            if self.end and event.time > self.end:
                break
            self.inform_all(event)
