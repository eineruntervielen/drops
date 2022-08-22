import random

from src.drops import Member, Event, EventQueue, ChannelOptions
from ..model.theater import Theater
from ..model.messages import Messages


class Moviegoer(Member):
    subscriptions = {
        Messages.CUSTOMER_ARRIVES: ChannelOptions(),
        Messages.THEATER_AD: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.movies_in_theater: list = []
        self.share(time=random.expovariate(1 / 0.5), message=Messages.CUSTOMER_ARRIVES)

    def theater_ad(self, e: Event):
        self.movies_in_theater = e.movies_in_theater

    def customer_arrives(self, e: Event):
        self.share(
            time=e.time + random.expovariate(1 / 0.5),
            message=Messages.CUSTOMER_ARRIVES,
            movie=random.choice(Theater.config['movies']),
            num_tickets=random.randint(1, 6)
        )
