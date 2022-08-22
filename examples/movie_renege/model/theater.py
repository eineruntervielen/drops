from src.drops import Member, Event, EventQueue, ChannelOptions
from ..model.messages import Messages


class Theater(Member):
    subscriptions = {
        Messages.CUSTOMER_ARRIVES: ChannelOptions(),
    }
    config = dict(
        movies=['Python Unchained', 'Kill Process', 'Pulp Implementation'],
    )

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        e = Event(time=0, message=Messages.THEATER_AD, movies_in_theater=self.config['movies'])
        self._event_queue.put(e)

    def customer_arrives(self, e: Event):
        print(e)
