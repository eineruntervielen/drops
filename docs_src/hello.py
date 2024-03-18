from drops import DelayedEvent, Drops, Event


def foo(e: Event):
    print("Hello " + e.body.get("greeter"))
    return DelayedEvent(msg="say_goodbye", delay_s=1, body={"name": "Alice"})


def bar(e: Event):
    print("Goodbye " + e.body.get("name"))


if __name__ == "__main__":
    drops = Drops(__name__)

    drops.register_callback(foo, ("say_hello",), )
    drops.register_callback(bar, ("say_goodbye",))

    # Kick-off event
    drops.event_queue.put(Event(event_id=0, msg="say_hello", time=0, body={"greeter": "Alice"}))

    drops.run()
