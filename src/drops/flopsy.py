from __future__ import annotations

from inspect import isfunction, isgeneratorfunction
from itertools import count
from queue import PriorityQueue
from typing import Any, Callable, Iterable, MutableMapping, NamedTuple, Optional

AnyDict = dict[str, Any]


class Publishing(NamedTuple):
    msg: str
    delay_h: int = 0
    delay_m: int = 0
    delay_s: int = 0
    body: AnyDict = {}


class Event(NamedTuple):
    event_id: int
    msg: str
    time: int
    # sender: str
    body: AnyDict  # simplenamespace wäre cooler


EventCallback = Callable[[Event], Optional[Publishing]]
Handler = type | Callable[[...], EventCallback]


class EventQueue(PriorityQueue[Event]):

    def __init__(self, maxsize: int) -> None:
        super().__init__(maxsize)
        self.channels: MutableMapping[str, list[Handler]] = {}

    def add_handler_to_channel(self, msg: str, handler: Handler):
        self.channels[msg].append(handler)

    def open_new_channel(self, msg: str) -> None:
        if not self.channels.get(msg):
            self.channels[msg] = []


class Flopsy:
    event_counter = count()

    def __init__(self: Flopsy, name: str, maxsize: int = -1, end: Optional[int] = None) -> None:
        self.name = name
        self.now = 0
        self.end = end
        self.event_queue = EventQueue(maxsize=maxsize)

    def register_handler(self, msg: str, handler: Handler):
        self.event_queue.open_new_channel(msg)
        self.event_queue.add_handler_to_channel(msg, handler)

    def register_source(self):
        raise NotImplementedError(
            "hier sollen alle sourcen eingesetzt werden, die werden alle einmal aufgerufen damit initiale events da sind.")

    def register_callback(self, func: Callable[[...], EventCallback], msgs: Iterable[str]):
        for msg in msgs:
            self.register_handler(msg, func)

    def register_class(self, cls: type, **kwargs):
        inst = cls(**kwargs)
        for msg in inst.consumptions:
            self.register_handler(msg, inst)

    @staticmethod
    def call_member(member, event: Event) -> Publishing:
        if isfunction(member) or isgeneratorfunction(member):
            callback: EventCallback = member
        else:
            callback: EventCallback = getattr(member, event.msg)
        follow_up = callback(event)
        return follow_up

    def create_follow_up_event(self, pub: Publishing) -> Event:
        return Event(
            event_id=next(self.event_counter),
            msg=pub.msg,
            time=self.now + pub.delay_m,  # todo noch machen
            body=pub.body
        )

    def inform_all(self, event: Event) -> None:
        for member in self.event_queue.channels.get(event.msg, f"{event.msg} gibt es nicht"):
            if follow_up := self.call_member(member, event):
                new_event = self.create_follow_up_event(follow_up)
                self.event_queue.put(new_event)

    def dispatch(self) -> None:
        while not self.event_queue.empty():
            event = self.event_queue.get(block=False)
            self.now = event.time
            if self.end and event.time > self.end:
                break
            self.inform_all(event)
