import random
from enum import Enum
from src.drops import Drops, DropsMessage, Member, ChannelOptions, EventQueue, Event, Drops


class Messages(DropsMessage):
    DRIVING = ()
    PARKING = ()


class Car(Member):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.DRIVING: ChannelOptions(),
        Messages.PARKING: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self._event_queue.put(Event(
            time=0,
            message=Messages.PARKING,
        ))

    def _driving(self, e: Event):
        print(f'Car driving  {e.time}')
        self._event_queue.put(Event(
            time=e.time + random.randint(1, 10),
            message=Messages.PARKING,
        ))

    def _parking(self, e: Event):
        print(f'Car parking at {e.time}')
        self._event_queue.put(Event(
            time=e.time + random.randint(1, 10),
            message=Messages.DRIVING,
        ))


class Members(Enum):
    CAR = Car


app = Drops(
    messages=Messages,
    members=Members,
    end=100
)

app.run()
