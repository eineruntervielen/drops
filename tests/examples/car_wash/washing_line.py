from collections import deque
from dataclasses import dataclass

from drops.drops import DelayedEvent, Event


@dataclass
class WashingLine:
    consumptions = ("car_arrives", "start_wash", "end_wash")

    collected_dirt = 0
    waiting_line = deque()
    washing_position = deque(maxlen=1)

    @property
    def is_free(self) -> bool:
        return len(self.waiting_line) < 15

    def car_arrives(self, e: Event) -> DelayedEvent:
        car = e.body.get('car')
        self.waiting_line.append(car)
        if self.is_free:
            return DelayedEvent(msg="start_wash", delay_s=1, body={'car': car})
        return DelayedEvent(msg="stop_sending")

    def start_wash(self, e: Event) -> DelayedEvent:
        car = e.body.get('car')
        self.washing_position.append(car)
        return DelayedEvent(msg="end_wash", delay_s=6, body={"car": car})

    def end_wash(self, e: Event) -> None:
        import random

        current_dirt = e.body.get("car").dirt
        removed_dirt = round(random.uniform(0, current_dirt), 3)
        self.collected_dirt += removed_dirt
        print("removed dirt", removed_dirt)
        print("collected dirt in washing_line", self.collected_dirt)
