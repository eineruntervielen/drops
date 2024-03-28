__all__ = ["PaymentArea"]

import random
from collections import deque
from dataclasses import dataclass

from drops.core import DEvent, Event


@dataclass
class PaymentArea:
    consumptions = (
        "register_checkout",
        "customer_arrives",
        "customer_waiting_line",
    )
    checkouts = []
    waiting_line = deque()

    def get_next_checkout(self) -> None:
        return random.choice(self.checkouts) if self.checkouts else None

    def register_checkout(self, e: Event) -> list[DEvent]:
        checkout = e.body.get("checkout")
        self.checkouts.append(checkout)
        if self.waiting_line:
            return [
                DEvent(msg="customer_arrives", delay_s=1, body={"customer": customer})
                for customer in self.waiting_line
            ]

    def customer_arrives(self, e: Event) -> list[DEvent]:
        checkout = self.get_next_checkout()
        if checkout:
            return [DEvent(msg="customer_in_checkout", delay_s=1, body={**e.body, "checkout": checkout})]
        else:
            return [
                DEvent(msg="customer_waiting_line", delay_s=1, body=e.body),
                DEvent(msg="more_checkouts_needed", delay_s=2, body={})
            ]

    def customer_waiting_line(self, e: Event) -> None:
        customer = e.body.get("customer")
        self.waiting_line.append(customer)


