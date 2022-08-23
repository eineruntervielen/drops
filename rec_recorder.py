import random
from enum import Enum
from src.drops import Drops, DropsMessage, DropsComponent, ChannelOptions, EventQueue, Event, Drops


class Messages(DropsMessage):
    REGISTER = ()


class RECORDER(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        '*': ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)


app = Drops(
    messages=Messages,
    members={
    },
    end=100
)

app.run()
