import random
import datetime as dt

from src.drops import Member, Event, EventQueue, ChannelOptions
from examples.alice.model.messages import Messages


class Vendor(Member):
    subscriptions = {
        Messages.COIN_INSERTED: ChannelOptions(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def _coin_inserted(self, e: Event):
        print(f'coin inserted says vender')
        if random.randint(0,9) < 5:
            self._event_queue.put(
                Event(
                    time=e.time+dt.timedelta(minutes=2),
                    message=Messages.COIN_DETECTED
                )
            )
        else:
            self._event_queue.put(
                Event(
                    time=e.time+dt.timedelta(minutes=2),
                    message=Messages.COIN_ERROR
                )
            )

            


