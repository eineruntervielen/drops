"""0. Car

This example shows a car starting to drive, then parking, alternating until the simulation reaches time 100
"""
import random
from src.drops import Drops, DropsMessage, DropsComponent, MessageFilter, EventQueue, Event

__all__ = ['Messages', 'Car']


class Messages(DropsMessage):
    DRIVING = ()
    PARKING = ()


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, MessageFilter] = {
        Messages.DRIVING: MessageFilter(),
        Messages.PARKING: MessageFilter()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.is_driving: bool = False
        self.share(time=0, msg=Messages.DRIVING)

    def driving(self, event: Event):
        print(f'Car driving at {event.time}')
        time_driving = event.time + random.randint(4, 10)
        self.share(
            time=time_driving,
            msg=Messages.PARKING,
        )

    def parking(self, event: Event):
        print(f'Car parking at {event.time}')
        time_parking = event.time + random.randint(8, 10)
        self.share(
            time=time_parking,
            msg=Messages.DRIVING,
        )


def main():
    app = Drops(
        messages=Messages,
        members={
            'car': Car,
        },
        end=100
    )

    app.run()


if __name__ == '__main__':
    main()
