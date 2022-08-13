from src.drops import Member, Event, EventQueue, ChannelOptions
from examples.alice.model.messages import Messages


class Vendor(Member):
    subscriptions = {
        Messages.COIN_INSERTED: ChannelOptions(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def coin_inserted(self, e: Event):
        print(f'coin inserted says vender')
