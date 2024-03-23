from random import random
from itertools import count
from typing import Optional

from drops import DEvent, Event


def finite_car_source_maker(num_cars: int):
    counter = count(start=0, step=1)

    def car_source(e: Optional[Event]) -> DEvent:
        car_id = next(counter)
        while num_cars - car_id > 0:
            return DEvent(
                msg="car_arrives",
                delay_s=5,
                body={"car": Car(car_id=car_id, dirt=random())}
            )

    car_source.consumptions = ("car_arrives",)
    return car_source
