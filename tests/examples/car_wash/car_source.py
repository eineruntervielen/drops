from random import randint
from typing import Optional

from drops.core import DEvent, Event, EventCallback
from tests.examples.car_wash.car import Car, make_car


def car_source_gen(num_cars: int) -> EventCallback:
    counter = 0
    send = True

    def car_source(e: Optional[Event]) -> DEvent:
        nonlocal counter
        nonlocal send
        if counter >= num_cars:
            send = False

        rnd = randint(10, 25)
        t = e.time if e else 0
        while send:
            counter += 1
            return DEvent(msg="car_arrives", delay_s=rnd, body={"car": make_car(counter)})

    return car_source


"""Completely different example"""

from random import random
from itertools import count


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

    return car_source


"""Completely different example"""


def finite_car_source2(num_cars: int):
    for id in range(num_cars):
        yield DEvent(
            msg="car_arrives",
            delay_s=5,
            body={"car": Car(car_id=id, dirt=random())}
        )
