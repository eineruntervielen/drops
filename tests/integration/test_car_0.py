import unittest
from random import seed
from src.drops import Drops
from examples.single_file_example.car_0 import *


class TestCar0(unittest.TestCase):
    def test_complete_model(self):
        seed(0)
        app = Drops(
            messages=Messages,
            members={
                'car': Car,
            },
            end=100
        )

        app.run()


if __name__ == '__main__':
    unittest.main()
