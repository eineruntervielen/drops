import random
from typing import NamedTuple


class Car(NamedTuple):
    car_id: int
    dirt: float


def make_car(counter: int) -> Car:
    return Car(car_id=counter, dirt=round(random.uniform(0.2, 1), 2))
