import unittest

from drops.drops import Drops, Event
from tests.examples.car_wash.car_wash import WashingLine, gen_car


class TestCarWash(unittest.TestCase):
    def test_flow(self):
        drops = Drops(name=__name__, end=100)
        # drops.register_callback(func=car_source_maker(), msgs=['car_arrives', 'stop_sending'])
        drops.register_callback(func=gen_car, msgs=["car_arrives", "stop_sending"])
        drops.register_class(cls=WashingLine)
        drops.event_queue.put(Event(msg="car_arrives", time=0, payload={}))
        drops.dispatch()


if __name__ == "__main__":
    unittest.main()
