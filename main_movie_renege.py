import random

from enum import Enum
from src.drops import Drops, Member, DropsMessage, ChannelOptions, Event, EventQueue


class Messages(DropsMessage):
    """All messages that can be used for transferring information between two or
    more Members.
    """
    THEATER_AD = ()
    CUSTOMER_ARRIVES = ()


class Theater(Member):
    subscriptions = {
        Messages.CUSTOMER_ARRIVES: ChannelOptions(),
    }
    MOVIES = ['Python Unchained', 'Kill Process', 'Pulp Implementation']
    TICKETS = {m: 50 for m in MOVIES}

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.num_rejected_customers = 0
        self._event_queue.put(
            Event(time=0, message=Messages.THEATER_AD, movies_in_theater=self.MOVIES)
        )

    def customer_arrives(self, e: Event):

        ...
        # TODO implement


class Moviegoer(Member):
    subscriptions = {
        Messages.CUSTOMER_ARRIVES: ChannelOptions(),
        Messages.THEATER_AD: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.movies_in_theater: list = []
        # Release first customer
        self.share(time=random.expovariate(1 / 0.5), message=Messages.CUSTOMER_ARRIVES)

    def theater_ad(self, e: Event):
        self.movies_in_theater = e.movies_in_theater

    def customer_arrives(self, e: Event):
        self.share(
            time=e.time + random.expovariate(1 / 0.5),
            message=Messages.CUSTOMER_ARRIVES,
            movie=random.choice(self.movies_in_theater),
            num_tickets=random.randint(1, 6)
        )


class Members(Enum):
    THEATER = Theater  # todo order matters, not good
    MOVIEGOER = Moviegoer


def main():
    app = Drops(
        messages=Messages,
        members=Members
    )
    app.run()


if __name__ == '__main__':
    main()
