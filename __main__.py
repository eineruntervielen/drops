import datetime as dt

from src.drops import Drops, Event
from model.members import Members
from model.messages import Messages

NOW = dt.datetime.now()

members = {
    'name_alice': Members.ALICE,
    'name_bob': Members.BOB
}

sim = Drops(
    messages=Messages,
    members=members
)

e = Event(time=NOW, message=Messages.HELLO)
sim.event_queue.queue.put(e)
sim.run()