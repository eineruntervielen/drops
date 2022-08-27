from random import randint
import logging
from dataclasses import dataclass

from src.drops import Drops, DropsMessage, DropsComponent, MessageFilter, EventQueue, Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class M(DropsMessage):
    OCCUPY = ()
    FREE = ()
    REQUEST_FREE_SLOTS = ()
    RESPOND_FREE_SLOTS = ()
    DRIVING = ()
    PARKING = ()
    REGISTER_SLOT = ()


@dataclass
class Coordinate:
    x: int
    y: int

    def __iadd__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def distance(self):
        return abs(self.x) + abs(self.y)

    def time_driving(self):
        return abs(self.x) + abs(self.y)


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, MessageFilter] = {
        M.DRIVING: MessageFilter(),
        M.PARKING: MessageFilter(),
        M.RESPOND_FREE_SLOTS: MessageFilter()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.battery_state = 1
        self.coord: Coordinate = Coordinate(x=0, y=0)
        # Set impuls to start driving, in method is check if possible or not
        # self.share(time=0, msg=M.DRIVING, coord=self.coord)
        self.share(time=50, msg=M.REQUEST_FREE_SLOTS)

    def driving(self, e: Event):
        if self.battery_state > 0:
            distances = Coordinate(randint(-5, 5), randint(-5, 5))
            time_driving = distances.time_driving()
            self.coord += distances
            self.share(time=e.time + time_driving, msg=M.PARKING, coord=self.coord)
            logger.info(f'{self.name} t={e.time} \tstart driving from \t{e.coord} with distances {distances}')

    def parking(self, e: Event):
        logger.info(f'{self.name} t={e.time} \tstart parking at \t{e.coord}')
        time_pausing = randint(1, 10)
        self.share(time=e.time + time_pausing, msg=M.DRIVING, coord=e.coord)

    def respond_free_slots(self, e: Event):
        print(e.slots)



class ParkingSystem(DropsComponent):
    subscriptions: dict[DropsMessage, MessageFilter] = {
        M.REGISTER_SLOT: MessageFilter(),
        M.REQUEST_FREE_SLOTS: MessageFilter()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.parking_slots: dict[str, bool] = {}

    def register_slot(self, e: Event):
        self.parking_slots[e.sender] = False  # every slot is free at startup design decision

    def occupy(self, e: Event):
        self.parking_slots[e.sender] = True

    def free(self, e: Event):
        self.parking_slots[e.sender] = False

    def request_free_slots(self, e: Event):
        free_slots = [slot for slot in self.parking_slots if self.parking_slots[slot] is False]
        self.share(time=e.time + 2, msg=M.RESPOND_FREE_SLOTS, slots=free_slots)


class ParkingSlot(DropsComponent):
    subscriptions: dict[DropsMessage, MessageFilter] = {
        M.OCCUPY: MessageFilter(),
        M.FREE: MessageFilter()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.occupied = False
        self.share(time=0, msg=M.REGISTER_SLOT)
        self.share(time=randint(10, 20), msg=M.OCCUPY, occupy=True)  # occupy the slot at this time in the future

    def occupy(self, e: Event):
        self.occupied = True
        logger.info(f'{self.name} is at time {e.time} {self.occupied=}')
        self.share(time=e.time + randint(10, 20), msg=M.FREE)

    def free(self, e: Event):
        self.occupied = False
        logger.info(f'{self.name} is at time {e.time} {self.occupied=}')
        self.share(time=e.time + randint(10, 20), msg=M.OCCUPY)


Members = {
    'car': Car,
    'slot': ParkingSlot,
    'parking_system': ParkingSystem
}

app = Drops(
    messages=M,
    members=Members,
    end=100
)

app.run()
