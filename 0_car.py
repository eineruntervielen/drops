import random
from enum import Enum
from src.drops import Drops, DropsMessage, DropsComponent, ChannelOptions, EventQueue, Event, Drops


class Messages(DropsMessage):
    DRIVING = ()
    PARKING = ()


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.DRIVING: ChannelOptions(),
        Messages.PARKING: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def driving(self, e: Event):
        print(f'Car driving  {e.time}')
        self._event_queue.put(Event(
            time=e.time + random.randint(4, 10),
            message=Messages.PARKING,
        ))

    def parking(self, e: Event):
        print(f'Car parking at {e.time}')
        self._event_queue.put(Event(
            time=e.time + random.randint(1, 4),
            message=Messages.DRIVING,
        ))


app = Drops(
    messages=Messages,
    members={
        'car1': Car,#
    },
    end=100
)

app.run()
