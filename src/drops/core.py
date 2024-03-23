from __future__ import annotations

import time
import types
import typing
from inspect import isfunction, isgeneratorfunction
from itertools import count
from queue import PriorityQueue
from typing import Any, Callable, Iterable, MutableMapping, NamedTuple, Optional

AnyDict = dict[str, Any]


class DelayedEvent(NamedTuple):
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

    def __lt__(self, other: Event) -> bool:
        return (
                self.time < other.time
                or self.time == other.time
                and self.event_id < other.event_id
        )


EventCallback = Callable[[Optional[Event]], Optional[DelayedEvent]]
Handler = type | Callable[[...], EventCallback]


class EventQueue(PriorityQueue[Event]):

    @staticmethod
    def call_member(member, event: Event) -> DelayedEvent:
        if isfunction(member) or isgeneratorfunction(member):
            callback: EventCallback = member
        else:
            callback: EventCallback = getattr(member, event.msg)
        follow_up = callback(event)
        return follow_up

    def __init__(self, maxsize: int) -> None:
        super().__init__(maxsize)
        self.channels: MutableMapping[str, list[Handler]] = {}

    def add_handler_to_channel(self, msg: str, handler: Handler):
        self.channels[msg].append(handler)

    def open_new_channel(self, msg: str) -> None:
        if not self.channels.get(msg):
            self.channels[msg] = []


class Drops:
    event_counter = count()

    def __init__(self: Drops, name: str, maxsize: int = -1, end: Optional[int] = None) -> None:
        self.name = name
        self.now = 0
        self.end = end
        self.event_queue = EventQueue(maxsize=maxsize)
        self.json_schema = []

    def register_handler(self, msg: str, handler: Handler):
        self.event_queue.open_new_channel(msg)
        self.event_queue.add_handler_to_channel(msg, handler)

    def register_source(self, func, call_initial: bool) -> None:
        for msg in getattr(func, "consumptions"):
            self.register_handler(msg, func)
        # TODO: how to manage initial event
        # call for initial event
        if call_initial:
            if follow_up := func(None):
                if isinstance(follow_up, list):
                    for fup in follow_up:
                        new_event = self.create_follow_up_event(fup)
                        self.event_queue.put(new_event)
                else:
                    new_event = self.create_follow_up_event(follow_up)
                    self.event_queue.put(new_event)

    def register_callback(self, func: Callable[[...], EventCallback], msgs: Iterable[str]):
        for msg in msgs:
            self.register_handler(msg, func)

    def register_module(self, mod: types.ModuleType):
        import inspect
        mems = dict(inspect.getmembers_static(mod))
        for msg in mems.get("__all__"):
            self.register_handler(msg, mems.get(msg))

    def register_instance(self, inst: Any):
        self.json_schema.append(inst)
        for msg in inst.consumptions:
            self.register_handler(msg, inst)

    def create_follow_up_event(self, pub: DelayedEvent) -> Event:
        return Event(
            event_id=next(self.event_counter),
            msg=pub.msg,
            time=self.now + pub.delay_s,  # todo noch machen
            body=pub.body
        )

    def inform_all(self, event: Event) -> None:
        for member in self.event_queue.channels.get(event.msg):
            if follow_up := EventQueue.call_member(member, event):
                if isinstance(follow_up, list):
                    for fup in follow_up:
                        new_event = self.create_follow_up_event(fup)
                        self.event_queue.put(new_event)
                else:
                    new_event = self.create_follow_up_event(follow_up)
                    self.event_queue.put(new_event)

    def run(self, timeout_s: float = 0) -> None:
        while not self.event_queue.empty():
            event = self.event_queue.get(block=False)
            time.sleep(timeout_s)
            self.now = event.time
            if self.end and event.time > self.end:
                break
            self.inform_all(event)

    def run_return(self, timeout_s: float) -> Any:
        while not self.event_queue.empty():
            event = self.event_queue.get(block=False)
            time.sleep(timeout_s)
            self.now = event.time
            if self.end and event.time > self.end:
                break
            self.inform_all(event)
            # blabla
            return self

    def run_with_cb_while(self, cb: Callable[[dict[str, Any]], Any], pred: bool) -> None:
        while pred:
            self.run_return(timeout_s=1)
            c = {
                str(thing): thing.JSON() for thing in self.json_schema
            }
            body = dict(current_time=self.now, **c)
            cb(body)
