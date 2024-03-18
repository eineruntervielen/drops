import random
from typing import Optional

from drops.core import DelayedEvent, Event, EventCallback
from tests.examples.car_wash.car import make_car


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
