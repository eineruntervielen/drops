import logging
import random

from src.drops import Producer, Event
from tests.examples.emergency_department.ae_patient import AEPatient


class AEPatientSource(Producer):
    consumptions = ["PATIENT_ARRIVED"]
    SAMPLED_INTER_ARRIVAL = 5

    def __init__(self, name, event_queue):
        super().__init__(name, event_queue)
        self.publish(time=0, msg="PATIENT_ARRIVED", patient=next(self.generate()))

    def generate(self):
        yield AEPatient()

    def patient_arrived(self, e: Event) -> None:
        logging.debug(msg=f"arrived {e.time} again at aepaetientsource")
        new_time = e.time + random.expovariate(1.0 / 5)
        self.publish(time=new_time, msg="PATIENT_ARRIVED", patient=next(self.generate()))
