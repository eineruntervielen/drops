"""2. Car


Two cars no ignition
"""
import random
from src.drops import Drops, DropsMessage, DropsComponent, ChannelOptions, EventQueue, Event


class Messages(DropsMessage):
    DRIVING = ()
    PARKING = ()


class Car(DropsComponent):
    subscriptions: dict[DropsMessage, ChannelOptions] = {
        Messages.DRIVING: ChannelOptions(filter_am_i_receiver=True),
        Messages.PARKING: ChannelOptions(filter_am_i_receiver=True)
    }

    def __init__(self, name: str, event_queue: EventQueue):
        super().__init__(name, event_queue)

    def driving(self, event: Event):
        print(f'Car driving at {event.time}')
        time_driving = event.time + random.randint(4, 10)
        self.share(
            time=time_driving,
            message=Messages.PARKING,
        )

    def parking(self, event: Event):
        print(f'Car parking at {event.time}')
        time_parking = event.time + random.randint(8, 10)
        self.share(
            time=time_parking,
            message=Messages.DRIVING,
        )


app = Drops(
    messages=Messages,
    members={
        'car1': Car,
        'car2': Car,
    },
    end=100
)

app.event_queue.put(
    Event(
        time=0,
        message=Messages.DRIVING,
        receiver='car1'
    )
)

app.run()
