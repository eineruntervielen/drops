from src.drops import Member, Event, EventQueue, ChannelOptions
from ..model.messages import Messages


class Controler(Member):
    subscriptions = {
        Messages.CAR_LEAVES: ChannelOptions(),
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.share(
            time=0,
            message=Messages.CAR_ARRIVES
        )

    def car_arrives(self, e: Event):
        self.share(time=e.time + 5, message=Messages.START_WASHING)

    def car_leaves(self, e: Event):
        ...
