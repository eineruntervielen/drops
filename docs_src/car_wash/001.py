from typing import Annotated, NamedTuple


class Car(NamedTuple):
    car_id: Annotated[int, "Positive integer greater than 0"]
    dirt: Annotated[float, "Real number between 0 and 1"]
