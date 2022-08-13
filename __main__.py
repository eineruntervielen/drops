import json
import importlib
import datetime as dt

from pathlib import Path
from re import M
from src.drops import Drops
from examples.aliceandbob.model.members import Members
from examples.aliceandbob.model.messages import Messages


def main():

    app = Drops(
        messages=Messages,
        members=Members)
    app.run()
    print('rausgekommen')


if __name__ == '__main__':
    main()
