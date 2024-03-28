__all__ = (
    "customer_arrives",
    "register_checkout",
    "customer_in_checkout",
    "start_payment",
    "end_payment",
    "stop_sending",
    "queueing_at_checkout",
    "customers_in_queue",
    "customer_waiting_line",
    "more_checkouts_needed",
    "checkout_can_be_closed"
)


def customer_arrives(e) -> None:
    customer = e.body.get("customer")
    print(f"{e.time:<10}{customer} arriving at the payment area")


def register_checkout(e) -> None:
    checkout = e.body.get("checkout")
    print(f"{e.time:<10}Register {checkout}")


def customer_in_checkout(e) -> None:
    checkout = e.body.get("checkout")
    customer = e.body.get("customer")
    print(f"{e.time:<10}{customer} in {checkout} queue")


def customer_waiting_line(e) -> None:
    customer = e.body.get("customer")
    print(f"{e.time:<10}Putting {customer} in waiting line")


def queueing_at_checkout(e) -> None:
    customer = e.body.get("customer")
    checkout = e.body.get("checkout")
    print(f"{e.time:<10}{customer} choose {checkout}")


def customers_in_queue(e) -> None:
    checkout = e.body.get("checkout")
    print(f"{e.time:<10}Customers queue at {checkout}")


def start_payment(e) -> None:
    checkout = e.body.get("checkout")
    customer = e.body.get("customer")
    print(f"{e.time:<10}{customer} starts paying on {checkout}")


def end_payment(e) -> None:
    customer = e.body.get("customer")
    print(f"{e.time:<10}{customer} leaving payment area")


def stop_sending(e) -> None:
    print(f"{e.time:<10}Stopping sending event")


def more_checkouts_needed(e) -> None:
    print(f"{e.time:<10}Too much customers, need a new checkout")


def checkout_can_be_closed(e) -> None:
    print(f"{e.time:<10}A checkout can be closed")
