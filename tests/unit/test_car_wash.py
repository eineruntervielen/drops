import unittest

from drops import Drops
from tests.examples.car_wash import finite_car_source_maker


class AllExamplesTest(unittest.TestCase):
    def test_example_car_wash(self):
        from tests.examples.car_wash import WashingLine, car_source_gen, car_logging

        drops = Drops(__name__)
        drops.register_source(car_source_gen(), call_initial=True)
        drops.register_instance(WashingLine())
        drops.register_module(car_logging)
        drops.run()

    def test_example_car_wash_finite(self):
        from tests.examples.car_wash import WashingLine, car_logging

        drops = Drops(__name__)
        drops.register_source(finite_car_source_maker(num_cars=5), call_initial=True)
        drops.register_instance(WashingLine())
        drops.register_module(car_logging)
        drops.run()


if __name__ == '__main__':
    unittest.main()
