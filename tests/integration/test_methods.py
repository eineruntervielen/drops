import unittest

from src.drops import Drops, Event
from tests.examples.car_wash.car_wash import WashingLine, car_source_maker


class TestCarWash(unittest.TestCase):
    def test_flow(self):
        drops = Drops(name=__name__, end=100)
        drops.register_callback(func=car_source_maker(), msgs=['car_arrives', 'stop_sending'])
        drops.register_class(cls=WashingLine)
        drops.event_queue.put(Event(msg="car_arrives", time=0, payload={}))
        drops.run()


if __name__ == '__main__':
    unittest.main()