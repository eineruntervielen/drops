import random
from enum import Enum
from src.drops import Drops, DropsMessage, DropsComponent, ChannelOptions, EventQueue, Event, Drops


class Messages(DropsMessage):
    REGISTER = ()


class Recorder(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.REGISTER: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def register(self, e):
        print(e)


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {

    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.share(
            time=0,
            message=Messages.REGISTER,
            sender=self
        )


app = Drops(
    messages=Messages,
    members={
        'rec': Recorder,
        'car': Car
    },
    end=100
)

app.run()
