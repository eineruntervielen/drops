import tests.examples.car_wash.car_logging as car_logging

from drops.drops import Drops
from tests.examples.car_wash.car_source import car_source_gen
from tests.examples.car_wash.washing_line import WashingLine

if __name__ == '__main__':
    flopsy = Drops(name=__name__, end=100)
    flopsy.register_source(func=car_source_gen())
    flopsy.register_class(cls=WashingLine)
    flopsy.register_module(mod=car_logging)
    flopsy.run()
