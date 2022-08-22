import datetime as dt
from src.drops import ChannelOptions, EventQueue, Event, Member
from examples.alice.model.messages import Messages


class Alice(Member):
    subscriptions = {
        Messages.COIN_DETECTED: ChannelOptions(),
        Messages.COIN_ERROR: ChannelOptions(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self._event_queue.put(
            Event(
                time=dt.datetime.now(),
                message=Messages.COIN_INSERTED,
                value='1 USD'
            )
        )

    def _coin_detected(self, e: Event):
        print('coin detected')

    def _coin_error(self, e: Event):
        print('coin error')
