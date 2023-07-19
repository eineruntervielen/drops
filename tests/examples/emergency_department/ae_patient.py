import random
from dataclasses import dataclass, field
from itertools import count


@dataclass
class AEPatient:
    time_in_system: int = 0
    patient_id: int = field(default_factory=count().__next__, init=False)
    priority: float = field(default_factory=lambda: random.choices([1, 2, 3, 4, 5], [0.1, 0.2, 0.4, 0.2, 0.1])[0])

