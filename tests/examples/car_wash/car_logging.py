__all__ = ("car_arrives", "start_wash")


def car_arrives(e) -> None:
    """print the arrival event"""
    print(f"A car with Id = {e.body.get("car")} arrived at {e.time}")


def start_wash(e) -> None:
    """print the start wash event"""
    print(f"Start washing of {e.body.get('car')}")


def end_wash(e) -> None:
    """print the end wash event"""
    print(f"End washing of {e.body.get('car')}")
