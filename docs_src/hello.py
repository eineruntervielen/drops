from drops import DEvent, Drops, Event


def foo(e: Event):
    print("Hello " + e.body.get("greeter"))
    return DEvent(msg="say_goodbye", delay_s=1, body={"name": "Alice"})


def bar(e: Event):
    print("Goodbye " + e.body.get("name"))


if __name__ == "__main__":
    drops = Drops()

    drops.register_callback(foo, "say_hello")
    drops.register_callback(bar, "say_goodbye")

    # Publish a message with no delay and a given body into the queue.
    # After the broker receives this message, follow-up events will be
    # triggered until everything inside the queue is consumed.
    drops.enqueue(msg="say_hello", delay_s=0, body={"greeter": "Alice"})

    drops.run()
