import logging
from collections import deque
from math import ceil
from queue import Queue
from random import uniform

import numpy as np
import pyaudio
from rpi_ws281x import Color, PixelStrip


class ChristmasLights(PixelStrip):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.alpha: float = 1
        self.sparkle: int = 0  # Chance of an LED being on is 1 / (n + 1)
        self.chasing: float = 0  # Time till next light
        self.breathing: float = 0  # Time for one cycle
        self.decibels: float = 0  # Maximum decibels for pattern
        self.pattern: list = ["#FFFFFF"]
        self.num_starts = 1
        self.active = list(range(100))  # TODO: Find led var name

        # Set up audio device
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNKS_PER_SECOND = 8
        CHUNK = round(RATE / CHUNKS_PER_SECOND)

        self.q = Queue()
        self.buffer = deque(maxlen=1)
        self.stream = pyaudio.PyAudio().open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            stream_callback=self._callback,
            frames_per_buffer=CHUNK,
        )

    def _calculate_db(self, sig):
        """
        Calculate the decibel level of a signal.
        """
        rms = np.sqrt(np.mean(sig**2))  # Root Mean Square
        if rms > 0.01:
            try:
                return (max(20 * np.log10(rms), 0) - 21) ** 1.5  # Convert to dB
            except:
                return 0
        return 0  # Handle silence

    def _callback(self, input_data, frame_count, time_info, flags):
        sig = np.frombuffer(input_data, dtype=np.int16)
        self.q.put_nowait(self._calculate_db(sig))  # Pass audio data to the queue
        return input_data, pyaudio.paContinue

    def _hex2rgb(self, hexcode: str) -> tuple[int, int, int]:
        code = hexcode.lstrip("#")
        return tuple(int(code[i : i + 2], 16) for i in (2, 0, 4))

    def setPattern(self, pattern: dict) -> None:
        logging.info(f"Changing pattern to {pattern['name']}")
        self.pattern = pattern["pattern"]
        self.sparkle = pattern["effects"]["sparkle"]
        self.chasing = pattern["effects"]["chasing"]
        self.breathing = pattern["effects"]["breathing"]
        self.decibels = pattern["effects"]["decibels"]
        self.alpha = 1
        self.active = list(range(100))  # TODO: Find led var name
        self.num_starts = (
            100  # TODO: Find led var name
            * (len(self.pattern) - 1)
            + 1
        )
        if self.decibels:
            self.long_pattern = [
                col
                for col in self.pattern
                for _ in range(100)  # This is the LED count TODO: Find var name
            ]
            self.start_index = 0

    def getSparkle(self) -> bool:
        return uniform(0, 1) >= self.sparkle  # NOQA

    def getSound(self) -> float:
        while not self.q.empty():
            self.buffer.append(self.q.get())
        if self.buffer:
            return sum(self.buffer) / len(self.buffer)
        return 0

    def getNewValue(self, pix: str, i: int) -> Color:
        rgb = self._hex2rgb(pix)
        # Apply sparkle
        if i not in self.active:
            return Color(0, 0, 0)
        # Apply breathing
        rgb = tuple([round(val * self.alpha) for val in rgb])
        return Color(*rgb)

    def setStrip(self):
        if not self.decibels:
            full_pattern = (self.pattern * ceil(self.numPixels() / len(self.pattern)))[
                : self.numPixels()
            ]
        else:
            full_pattern = self.long_pattern[self.start_index : self.start_index + 100][
                ::-1
            ]  # TODO: Find var name
        for i, pix in enumerate(full_pattern):
            self[i] = self.getNewValue(pix, i)
