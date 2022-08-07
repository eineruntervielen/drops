import json
import importlib
import datetime as dt

from pathlib import Path
from src.drops import Drops
from examples.aliceandbob.model.members import Members
from examples.aliceandbob.model.messages import Messages


def main():

    app = Drops(
        messages=Messages,
        members={
            'Alice': {
                'member': Members.ALICE,
                'coin_detection_probability': 0.5
            },
            'VendingMachine': Members.VENDER
        }
    )

    app.run()


if __name__ == '__main__':
    main()
