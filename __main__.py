import datetime as dt
from model.alice import Alice
from src.drops import Drops, Event
from model.members import Members
from model.messages import Messages

NOW = dt.datetime.now()

sim = Drops(
    messages=Messages,
    members=Members
)

e = Event(time=NOW, message=Messages.HELLO)
sim.event_queue.queue.put(e)
sim.run()