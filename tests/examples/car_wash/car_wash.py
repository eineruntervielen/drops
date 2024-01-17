from collections import deque
from dataclasses import dataclass

from drops.flopsy import Flopsy, Event, EventCallback, Publishing


def car_source_maker() -> EventCallback:
    counter = 0
    send = True

    def car_source(e: Event):
        nonlocal counter
        nonlocal send
        if e.msg == 'stop_sending':
            send = False

        while send:
            counter += 1
            return Publishing(msg="car_arrives", delay_s=5, body={"car_id": counter})

    return car_source


def gen_car(event: Event) -> Publishing:
    return Publishing(msg="car_arrives", delay_s=5, body={"car": 0})


@dataclass
class WashingLine:
    consumptions = ("car_arrives", "start_wash", "end_wash")

    waiting_line = deque()
    washing_position = deque(maxlen=1)

    @property
    def is_free(self) -> bool:
        return len(self.waiting_line) < 5

    def car_arrives(self, e: Event) -> Publishing:
        car = e.body.get('car')
        print(f"A {car} arrived at {e.time}")
        self.waiting_line.append(car)
        if not self.is_free:
            return Publishing(msg="stop_sending")
        return Publishing(msg="start_wash", delay_m=1, body={'car': car})

    def start_wash(self, e: Event) -> Publishing:
        car = e.body.get('car')
        self.washing_position.append(car)
        print(f"Start washing of {car}")
        return Publishing(msg="end_wash", delay_m=6)

    def end_wash(self, e: Event) -> None:
        car = e.body.get('car')
        self.washing_position.popleft()
        print(f"End washing of {car}")


if __name__ == '__main__':
    flopsy = Flopsy(name=__name__, end=100)
    flopsy.register_callback(func=gen_car, msgs=["car_arrives", "stop_sending"])
    flopsy.register_class(cls=WashingLine)
    flopsy.event_queue.put(Event(event_id=1, msg="car_arrives", time=0, body={}))
    flopsy.dispatch()
