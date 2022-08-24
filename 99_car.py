from email.message import Message
import random
from enum import Enum
from src.drops import Drops, DropsMessage, DropsComponent, ChannelOptions, EventQueue, Event, Drops


class Messages(DropsMessage):
    DRIVING = ()
    PARKING = ()
    REGISTER_SLOT = ()


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.DRIVING: ChannelOptions(),
        Messages.PARKING: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.share(
            time=0,
            message=Messages.PARKING,
        )

    def driving(self, e: Event):
        print(f'Car driving  {e.time}')
        self.share(
            time=e.time + random.randint(1, 10),
            message=Messages.PARKING,
        )

    def parking(self, e: Event):
        print(f'Car parking at {e.time}')
        self.share(
            time=e.time + random.randint(1, 10),
            message=Messages.DRIVING,
        )


class ParkingSystem(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.REGISTER_SLOT: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.parking_slots: list = []

    def register_slot(self, e: Event):
        self.parking_slots.append(e.sender)


class ParkingSlot(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.PARKING: ChannelOptions(),
        Messages.DRIVING: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.occupied = False
        self.slot = None
        self.share(
            time=0,
            message=Messages.REGISTER_SLOT,
            sender=self.name
        )

    def driving(self, e: Event):
        print(f'Car {e.sender} left parking slot')
        self.occupied = False

    def parking(self, e: Event):
        if self.occupied:
            print(f'No free slot')
        else:
            print(f'Car {e.sender} starts parking')
            self.occupied = True
            self.slot = e.sender


Members = {
    'car1': Car,
    'slot': ParkingSlot
}

app = Drops(
    messages=Messages,
    members=Members,
    end=100
)

app.run()
