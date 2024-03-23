import unittest

from drops import Drops
from tests.examples.car_wash import *


class AllExamplesTest(unittest.TestCase):
    def test_example_car_wash(self):
        drops = Drops()
        drops.register_source(car_source_gen(num_cars=5), "car_arrives", call_initial=True)
        drops.register_instance(WashingLine())
        drops.register_module(car_logging)
        drops.run()

    def test_example_car_wash_finite(self):
        drops = Drops()
        drops.register_source(finite_car_source_maker(num_cars=5), "car_arrives", call_initial=True)
        drops.register_instance(WashingLine())
        # drops.register_module(car_logging)
        drops.run()

    def test_example_car_wash_finite2(self):
        drops = Drops()
        drops.register_generator(finite_car_source2(num_cars=5), "car_arrives", call_initial=True)
        drops.register_instance(WashingLine())
        drops.register_module(car_logging)
        drops.run()


if __name__ == '__main__':
    unittest.main()
