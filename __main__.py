from src.drops import Drops
from pathlib import Path


def main():
    scenario = Path('examples/movie_renege')
    app = Drops(
        scenario_path=scenario
    )
    app.run()


if __name__ == '__main__':
    main()
