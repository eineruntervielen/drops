from collections import deque
from dataclasses import dataclass
from enum import StrEnum, auto

from drops.drops import Drops, Event, DelayedEvent


# class Messages(StrEnum):
#     PERSON_ARRIVED = auto()


def generate_patient(event: Event) -> DelayedEvent:
    return DelayedEvent(msg="person_arrived", delay=5)


@dataclass
class Receptionist:
    TIME_REGISTRATION_IN_MIN_MEAN = 2

    consumptions = ("person_arrived", "person_leaved_reception")
    queue = deque()

    def person_arrived(self, e: Event) -> DelayedEvent:
        """Do whatever the guy does when someone arrives at her queue """
        print("person kommt am reception an")
        self.queue.append(e.payload.get("person"))
        return DelayedEvent(
            msg="person_leaved_reception",
            delay=self.TIME_REGISTRATION_IN_MIN_MEAN
        )

    def person_leaved_reception(self, e: Event) -> DelayedEvent:
        """Remove person from registration place and send to nurse"""
        return DelayedEvent(
            msg="person_arrived_at_nurse",
            delay=0,
            payload={"person": self.queue.popleft()}
        )


@dataclass
class Nurse:
    consumptions = ("person_arrived_at_nurse", "person_leaved_nurse")
    TRIAGE_ACU = 0.2
    TRIAGE_ED = 0.8
    TIME_MEAN_TRIAGE = 5
    queue = deque()

    def person_arrived_at_nurse(self, e: Event) -> DelayedEvent:
        self.queue.append(e.payload.get("person"))
        return DelayedEvent(
            msg="person_leaved_nurse",
            delay=self.TIME_MEAN_TRIAGE,
            payload={}
        )

    def person_leaved_nurse(self, e: Event) -> DelayedEvent:
        print("person left nurse")


if __name__ == '__main__':
    drops = Drops(name=__name__, end=100)
    drops.register_callback(lambda e: DelayedEvent(msg="person_arrived", delay=5), msgs=('person_arrived',))
    drops.register_class(cls=Receptionist)
    drops.register_class(cls=Nurse)
    drops.event_queue.queue.append(Event(msg='person_arrived', time=0, payload={}))

    drops.dispatch()
