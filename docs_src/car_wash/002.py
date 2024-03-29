from itertools import count
from random import random

from drops import DEvent, Event
from tests.examples.car_wash.car import Car


def finite_car_source_maker(num_cars: int):
    counter = count()

    def car_source(e: Event) -> DEvent:
        car_id = next(counter)
        while num_cars - car_id > 0:
            return DEvent(
                msg="car_arrives",
                delay_s=5,
                body={"car": Car(car_id=car_id, dirt=random())}
            )

    return car_source
