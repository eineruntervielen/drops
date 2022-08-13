import datetime as dt
from src.drops import ChannelOptions, EventQueue, Member
from examples.alice.model.messages import Messages


class Alice(Member):
    subscriptions = {
        Messages.COIN_DETECTED: ChannelOptions(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.share(
            time=dt.datetime.now(),
            message=Messages.COIN_INSERTED
        )

    def coin_detected(self):
        ...

    def coin_error(self):
        ...
