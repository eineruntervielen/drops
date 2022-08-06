import datetime as dt

from types import MappingProxyType
from src.drops import ChannelOptions, Event, EventQueue, Member
from model.messages import Messages


class Alice(Member):
    default_config = MappingProxyType({
        'channels': {
            Messages.HELLO: ChannelOptions(),
            Messages.GOOD_BY: ChannelOptions()
        }
    })

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def hello(self, event: Event):
        self.event_queue.queue.put(
            Event(
                time=dt.datetime.now(),
                message=Messages.GOOD_BY,
            )
        )

    def good_by(self, event: Event):
        print('goodby from alice')
