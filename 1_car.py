"""1. Car


Produces infinite loop when we not terminate. Ignitions need to be there.
"""
import random
from src.drops import Drops, DropsMessage, DropsComponent, ChannelOptions, EventQueue, Event


class Messages(DropsMessage):
    DRIVING = ()
    PARKING = ()


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.DRIVING: ChannelOptions(),
        Messages.PARKING: ChannelOptions()
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)
        self.ignitions = 10

    def driving(self, event: Event):
        print(f'Car driving at {event.time}')
        self.ignitions -= 1
        time_driving = event.time + random.randint(4, 10)
        self.share(
            time=time_driving,
            message=Messages.PARKING,
        )

    def parking(self, event: Event):
        print(f'Car parking at {event.time}')
        if self.ignitions:
            time_parking = event.time + random.randint(8, 10)
            self.share(
                time=time_parking,
                message=Messages.DRIVING,
            )


app = Drops(
    messages=Messages,
    members={
        'car': Car,
    }
)

app.event_queue.put(
    Event(
        time=0,
        message=Messages.DRIVING,
    )
)

app.run()
