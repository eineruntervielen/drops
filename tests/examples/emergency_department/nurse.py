import random
from src.drops import Producer, Event
from tests.examples.emergency_department.ae_patient import AEPatient


class Nurse(Producer):
    consumptions = ["PATIENT_ARRIVED"]
    TRIAGE_TIME = 0  # fixme: genauer

    def __init__(self, name, event_queue):
        super().__init__(name, event_queue)

    def triage_patient(self, e):
        patient: AEPatient = e.patient
        new_time: float = e.time + self.TRIAGE_TIME
        match p := patient.priority:
            case _ if p == 5:
                # self.share(time=new_time, msg='PATIENT_ARRIVED_AE', patient=e.patient)
                print("patient go ae")
            case _ if p < 5:
                match d := random.choices(['HOME', 'MIU'], [0.2, 0.8])[0]:
                    case _ if d == "HOME":
                        # self.share(time=new_time, msg='PATIENT_ARRIVED_HOME', patient=e.patient)
                        print("patient go home")
                    case _ if d == "MUI":
                        # self.share(time=new_time, msg='PATIENT_ARRIVED_MIU', patient=e.patient)
                        print("patient go miu")

    def patient_arrived(self, e: Event) -> None:
        print(f"Patient with Id = {e.patient.patient_id} arrived at time = {e.time} at the Nurse")
        self.triage_patient(e)
