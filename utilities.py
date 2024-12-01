import math

import requests


def getPattern() -> dict:
    off = {
        "id": 1,
        "name": "Off",
        "pattern": ["#000000"],
        "active": True,
        "effects": {"breathing": 0, "chasing": 0, "sparkle": 0},
    }
    res = requests.get("http://192.168.1.92:81/patterns/active")
    if res.status_code == 200:  # NOQA
        return res.json()
    return off


def getAlpha(pps: float, elapsed: float) -> float:
    """
    Calculate the alpha value for Christmas lights preview.

    :param pps: Pulse Per Second. The number of complete waves which should occur per second.
    :param elapsed: The elapsed time in seconds
    :return: Alpha value for the light strip preview.
    """
    return (math.sin((2 * math.pi * pps) * elapsed) + 1) / 2


if __name__ == "__main__":
    getPattern()
