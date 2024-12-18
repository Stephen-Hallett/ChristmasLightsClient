import math
from threading import Timer

import requests

IP_ADDRESS = "192.168.1.12:81"


def getPattern() -> dict:
    default = {
        "id": 3,
        "name": "Peppermint",
        "pattern": ["#ffffff", "#ff0000", "#ffffff", "#00c90e"],
        "active": True,
        "effects": {"breathing": 0, "chasing": 0.09, "sparkle": 0, "decibels": 0},
    }
    try:
        res = requests.get(f"http://{IP_ADDRESS}/patterns/active")
        if res.status_code == 200:  # NOQA
            return res.json()
    except:
        pass
    return default


def getAlpha(pps: float, elapsed: float) -> float:
    """
    Calculate the alpha value for Christmas lights preview.

    :param pps: Pulse Per Second. The number of complete waves which should occur per second.
    :param elapsed: The elapsed time in seconds
    :return: Alpha value for the light strip preview.
    """
    return (math.sin((2 * math.pi * pps) * elapsed) + 1) / 2


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs) -> None:
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


if __name__ == "__main__":
    getPattern()
