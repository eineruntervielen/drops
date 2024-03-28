from random import randint
from typing import Optional

from drops.core import DEvent, Event, EventCallback
from tests.examples.shop.customer import make_customer


def customer_source_gen(num_customer: int) -> EventCallback:
    counter = 0
    send = True

    def customer_source(e: Optional[Event]) -> DEvent:
        nonlocal counter
        nonlocal send
        if counter >= num_customer:
            send = False

        time_after_last_customer = randint(1, 10)
        while send:
            counter += 1
            return DEvent(msg="customer_arrives",
                          delay_s=time_after_last_customer,
                          body={"customer": make_customer(counter)})
    return customer_source

