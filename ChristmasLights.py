import logging
from math import ceil
import time
from rpi_ws281x import PixelStrip, Color
from random import randint
"""Looks like the process is to do strip[i] = Color(r,g,b), then do strip.show() to update."""

class ChristmasLights(PixelStrip):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.alpha: float = 1
        self.sparkle: int = 0     # Chance of an LED being on is 1 / (n + 1)
        self.chasing: float = 0 # Time till next light
        self.breathing: float = 0 # Time for one cycle
        self.pattern: list = ["#FFFFFF"]

    def _hex2rgb(self, hexcode: str) -> tuple[int,int,int]:
        code = hexcode.lstrip('#')
        return tuple(int(code[i:i+2], 16) for i in (2, 0, 4))
    
    def setPattern(self, pattern:dict) -> None:
        logging.info(f'Changing pattern to "{pattern["name"]}"')
        self.pattern = pattern["pattern"]
        self.sparkle = pattern["effects"]["sparkle"]
        self.chasing = pattern["effects"]["chasing"]
        self.breathing = pattern["effects"]["breathing"]
        self.alpha = 1

    def getSparkle(self) -> bool:
        return randint(0, self.sparkle) == 0

    def getNewValue(self, pix: str) -> Color:
        rgb = self._hex2rgb(pix)
        # Apply sparkle
        if not self.getSparkle():
            logging.info("OFF")
            return Color(0,0,0)
        # Apply breathing
        rgb = tuple([round(val * self.alpha) for val in rgb])
        return Color(*rgb)

    def setStrip(self):
        full_pattern = (self.pattern * ceil(self.numPixels() / len(self.pattern)))[:self.numPixels()]
        for i, pix in enumerate(full_pattern):
            self[i] = self.getNewValue(pix)
        
