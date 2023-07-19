from collections import deque
from dataclasses import dataclass

from src.drops import DelayedEvent, Event, EventCallback


def car_source_maker() -> EventCallback:
    counter = 0
    send = True

    def car_source(e: Event):
        nonlocal counter
        nonlocal send
        if e.msg == 'stop_sending':
            send = False

        while send:
            counter += 1
            return DelayedEvent(msg="car_arrives", delay=5, payload={"car_id": counter})

    return car_source


@dataclass
class WashingLine:
    consumptions = ("car_arrives", "start_wash", "end_wash")

    waiting_line = deque()
    washing_position = deque()

    @property
    def is_free(self) -> bool:
        return len(self.waiting_line) < 5

    def car_arrives(self, e: Event) -> DelayedEvent:
        print(f"A {e.car} arrived at {e.time}")
        if not self.is_free:
            return DelayedEvent(msg="stop_sending", delay=0)
        self.waiting_line.append(e.car)
        return DelayedEvent(msg="start_wash", delay=1, payload=e.car)

    def start_wash(self, e: Event) -> DelayedEvent:
        self.washing_position.append(e.car)
        print(f"Start washing of {e.car}")
        return DelayedEvent(msg="end_wash", delay=6)

    def end_wash(self, e: Event):
        self.washing_position.popleft()
        print(f"End washing of {e.car}")
