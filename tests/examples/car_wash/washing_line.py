__all__ = ["WashingLine"]

import random
from collections import deque
from dataclasses import dataclass

from drops.core import DelayedEvent as DEvent
from drops.core import Event


@dataclass
class WashingLine:
    consumptions = (
        "car_arrives",
        "start_wash",
        "end_wash"
    )

    collected_dirt = 0
    waiting_line = deque()
    washing_position = deque(maxlen=1)
    time_washing = 8

    def car_arrives(self, e: Event) -> DEvent:
        car = e.body.get("car")
        print(f"t={e.time} arriving {car}")
        if len(self.washing_position) == 0:
            print(f"t={e.time} getting {car} from the event at start_wash and append to washing position")
            self.washing_position.append(car)
            return DEvent(msg="start_wash", delay_s=1, body=e.body)
        else:
            print(f"t={e.time} putting {car} in waiting line")
            self.waiting_line.append(car)

    def start_wash(self, e: Event) -> DEvent:
        return DEvent(msg="end_wash", delay_s=20, body={"car": e.body.get("car")})

    def end_wash(self, e: Event) -> DEvent:
        clean_car = self.washing_position.popleft()
        print(f"t={e.time} leaving system {clean_car}")
        removed_dirt = round(random.uniform(0, clean_car.dirt), 3)
        self.collected_dirt += removed_dirt
        if self.waiting_line:
            next_car = self.waiting_line.popleft()
            return DEvent(msg="car_arrives", delay_s=1, body={"car": next_car})
