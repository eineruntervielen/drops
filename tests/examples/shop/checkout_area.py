"""Checkout Area of a Shop"""
__all__ = ["CheckoutArea"]

from collections import deque
from dataclasses import dataclass, field

from drops.core import DEvent, Event
from tests.examples.shop.checkout import Checkout, make_checkout


@dataclass
class CheckoutArea:
    consumptions = (
        "register_checkout",
        "customer_in_checkout",
        "start_payment",
        "end_payment",
        "more_checkouts_needed",
        "checkout_can_be_closed",
        "rethink_checkouts"
    )

    processed_customer = 0
    checkouts: dict[int, Checkout] = field(default_factory=dict)
    queues: dict[int, deque] = field(default_factory=dict)
    payment_positions: dict[int, deque] = field(default_factory=dict)

    def register_checkout(self, e: Event):
        checkout = e.body.get("checkout")
        checkout_id = checkout.checkout_id
        self.checkouts[checkout_id] = checkout
        self.queues[checkout_id] = deque()
        self.payment_positions[checkout_id] = deque(maxlen=1)

    def reopen_or_new_checkout(self) -> int:
        checkout_numbers = set(self.checkouts.keys())
        return min(set(range(len(checkout_numbers) + 1)) - checkout_numbers)

    def customer_in_checkout(self, e: Event) -> DEvent:
        checkout = e.body.get("checkout")
        checkout_id = checkout.checkout_id
        customer = e.body.get("customer")
        if len(self.payment_positions[checkout_id]) == 0:
            self.payment_positions[checkout_id].append(customer)
            return DEvent(msg="start_payment", delay_s=1, body=e.body)
        else:
            self.queues[checkout_id].append(customer)
            return DEvent(msg="rethink_checkouts", delay_s=1, body={})

    def start_payment(self, e: Event) -> DEvent:
        checkout = e.body.get("checkout")
        customer = e.body.get("customer")
        time_needed = int(round(customer.number_products / checkout.speed))
        return DEvent(msg="end_payment", delay_s=time_needed, body=e.body)

    def end_payment(self, e: Event) -> DEvent:
        checkout = e.body.get("checkout")
        checkout_id = checkout.checkout_id
        self.payment_positions[checkout_id].popleft()
        self.processed_customer += 1
        if checkout_id not in self.queues:
            self.del_checkout_payment_position(checkout_id)

        elif len(self.queues[checkout_id]) > 0:
            next_customer = self.queues[checkout_id].popleft()
            return DEvent(msg="customer_in_checkout", delay_s=1,
                          body={"checkout": checkout, "customer": next_customer})

    def del_checkout_payment_position(self, checkout_id):
        if len(self.payment_positions[checkout_id]) == 0:
            del self.payment_positions[checkout_id]

    def more_checkouts_needed(self, e: Event) -> DEvent:
        new_checkout = self.reopen_or_new_checkout()
        return DEvent(msg="register_checkout",
                      delay_s=0,
                      body={"checkout": make_checkout(new_checkout)})

    def checkout_can_be_closed(self, e: Event) -> list[DEvent]:
        checkout_id_to_close, _ = min(self.queues.items(), key=lambda q: len(q[1]))
        self.checkouts.pop(checkout_id_to_close)
        self.del_checkout_payment_position(checkout_id_to_close)
        customers = self.queues.pop(checkout_id_to_close)
        return [
            DEvent(msg="customer_arrives",
                   delay_s=1,
                   body={"customer": customer})
            for customer in customers
        ]

    def rethink_checkouts(self, e: Event) -> DEvent:
        """count number customers. Close Checkouts if to less. Open checkouts if needed.

        Returns:

        """
        print([len(v) for v in self.queues.values()])
        if all([len(customers) > 2 for customers in self.queues.values()]):
            print("Open new one")
            return DEvent(msg="more_checkouts_needed", delay_s=1, body={})

        if all([len(customers) == 0 for customers in self.queues.values()]):
            print("Close one")
            return DEvent(msg="checkout_can_be_closed", delay_s=1, body={})
