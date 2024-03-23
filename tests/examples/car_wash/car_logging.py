__all__ = ("car_arrives", "start_wash", "stop_sending")


def car_arrives(e) -> None:
    """print the arrival event"""
    print(f"{e.time:<10}A car with Id = {e.body.get('car')} arrived at {e.time}")


def start_wash(e) -> None:
    """print the start wash event"""
    print(f"{e.time:<10}Start washing of {e.body.get('car')}")


def end_wash(e) -> None:
    """print the end wash event"""
    print(f"{e.time:<10}End washing of {e.body.get('car')}")


def stop_sending(e) -> None:
    """print stop sending event"""
    print(f"{e.time:<10}Stopping sending event")
