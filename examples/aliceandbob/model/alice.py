import datetime as dt
from types import MappingProxyType

from src.drops import ChannelOptions, EventQueue, Member, Event

from examples.aliceandbob.model.messages import Messages


class Alice(Member):
    default_config = MappingProxyType({
        'patience': 5,
        'channels': {
        }
    })

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.share(
            time=dt.datetime.now(),
            message=Messages.COIN_INSERTED
        )
