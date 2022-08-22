# Drops

## Standard API

### Basic Usage

```python
from enum import Enum
from drops import Drops, DropsMessage, Member, ChannelOptions, Event


class Messages(DropsMessage):
    HELLO = ()
    GOOD_BY = ()


class Alice(Member):
    subscriptions = {
        Messages.GOOD_BY: ChannelOptions()
    }


class Bob(Member):
    subscriptions = {
        Messages.HELLO: ChannelOptions()
    }


class Members(Enum):
    ALICE = Alice
    BOB = Bob


app = Drops(
    messages=Messages,
    members=Members
)

```

## Scenario API
Say your simulation model is becoming more complex, and you don't want to manage everything in a single file.
This is where the drops scenario-api comes in handy. Instead of handing over every component of a simulation 
you can also provide the path to a scenario.

```bash
aliceandbob
├── model
│   ├── __init__.py
│   ├── alice.py
│   ├── members.py
│   ├── messages.py
│   └── bob.py
└── scenario.json
```

A configuration of a simple `scenario.json` would look something like
```json
{
  "alice": "Alice",
  "bob": "Bob"
}
```
```python
from drops import Drops
from pathlib import Path

app = Drops(
    scenario=Path('examples/aliceandbob')
)

app.run()
```
