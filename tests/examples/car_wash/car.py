import random
from typing import NamedTuple


class Car(NamedTuple):
    ident: int
    dirt: float


def make_car(counter: int) -> Car:
    return Car(ident=counter, dirt=round(random.uniform(0.2, 1), 2))
