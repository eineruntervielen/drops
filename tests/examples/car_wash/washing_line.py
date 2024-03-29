from collections import deque
from dataclasses import dataclass
from random import uniform
from typing import TypedDict

from drops.core import DEvent, Event
from tests.examples.car_wash.car import Car


class CarArrival(TypedDict):
    car: Car


type Arrival = CarArrival
type StartWash = CarArrival
type EndWash = CarArrival


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

    def car_arrives(self, e: Event[CarArrival]) -> DEvent:
        car: Car = e.body.get("car")
        print(f"{e.time:<10}Car({car.car_id}|{car.dirt:.3f}) arriving at the WashingLine")
        print(" " * 10 + "Checking if washing position is occupied")
        if len(self.washing_position) == 0:
            print(f"{e.time:<10}getting {car} from the event at start_wash and append to washing position")
            self.washing_position.append(car)
            return DEvent(msg="start_wash", delay_s=1, body=e.body)
        else:
            print(f"{e.time:<10}putting {car} in waiting line")
            self.waiting_line.append(car)

    def start_wash(self, e: Event) -> DEvent:
        return DEvent(msg="end_wash", delay_s=self.time_washing, body={"car": e.body.get("car")})

    def end_wash(self, e: Event[EndWash]) -> DEvent:
        _, _, time, *_ = e
        clean_car = self.washing_position.popleft()
        print(f"{time:<10}leaving system {clean_car}")
        removed_dirt = round(uniform(0, clean_car.dirt), 3)
        self.collected_dirt += removed_dirt
        if self.waiting_line:
            next_car = self.waiting_line.popleft()
            return DEvent(msg="car_arrives", delay_s=1, body={"car": next_car})
