import math

import requests

IP_ADDRESS = "192.168.1.40:81"


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
