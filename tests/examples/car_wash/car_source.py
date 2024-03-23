import random
from typing import Optional

from drops.core import DelayedEvent, Event, EventCallback
from tests.examples.car_wash.car import Car, make_car


def car_source_gen() -> EventCallback:
    counter = 0
    send = True

    def car_source(e: Optional[Event]) -> DelayedEvent:
        nonlocal counter
        nonlocal send
        if counter >= 20:
            send = False

        rnd = random.randint(10, 25)
        t = e.time if e else 0
        while send:
            counter += 1
            return DelayedEvent(msg="car_arrives", delay_s=rnd, body={"car": make_car(counter)})

    car_source.consumptions = ("car_arrives",)
    return car_source


from random import random
from itertools import count


def finite_car_source_maker(num_cars: int):
    counter = count(start=0, step=1)

    def car_source(e: Optional[Event]) -> DelayedEvent:
        car_id = next(counter)
        while num_cars - car_id > 0:
            return DelayedEvent(
                msg="car_arrives",
                delay_s=5,
                body={"car": Car(car_id=car_id, dirt=random())}
            )

    car_source.consumptions = ("car_arrives",)
    return car_source
