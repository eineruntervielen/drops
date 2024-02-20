import random
from typing import NamedTuple, Optional

from drops.drops import DelayedEvent, Event, EventCallback


class Car(NamedTuple):
    ident: 0
    dirt: float


def make_car(counter: int) -> Car:
    return Car(ident=counter, dirt=round(random.uniform(0.2, 1), 2))


def send_car_every_5_sec(event: Event) -> DelayedEvent:
    ident = event.body.get("car").counter + 1
    return DelayedEvent(msg="car_arrives", delay_s=5, body={"car": make_car(ident)})


def car_source_gen() -> EventCallback:
    counter = 0
    send = True

    def car_source(e: Optional[Event]):
        _ = e
        nonlocal counter
        nonlocal send
        if counter >= 10:
            send = False

        while send:
            counter += 1
            return DelayedEvent(
                msg="car_arrives",
                delay_s=random.randint(4, 10),
                body={"car": make_car(counter)}
            )

    car_source.consumptions = ("car_arrives", "stop_sending", "end_wash")

    return car_source
