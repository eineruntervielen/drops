import datetime as dt

from src.drops import Member, Event, EventQueue, ChannelOptions
from ..model.messages import Messages


class WashingLine(Member):
    subscriptions = {
        Messages.START_WASHING: ChannelOptions(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def start_washing(self, e: Event):
        print(f'{self.name} is washing a car')


