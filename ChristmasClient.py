import math
import time
from functools import partial

from utilities import RepeatedTimer, getAlpha, getPattern

from ChristmasLights import ChristmasLights

# LED strip configuration:
LED_COUNT = 100  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

SPARKLE_REFRESH = 4


lights = ChristmasLights(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)


off = {
    "id": 1,
    "name": "Off",
    "pattern": ["#000000"],
    "active": True,
    "effects": {"breathing": 0, "chasing": 0, "sparkle": 0, "decibels": 0},
}


def update_chasing(lights: ChristmasLights) -> None:
    lights.pattern.insert(0, lights.pattern[-1])
    lights.pattern.pop(-1)


chasing_update = partial(update_chasing, lights)


def update_sparkle(lights: ChristmasLights) -> None:
    lights.active = [lights.getSparkle() for _ in range(LED_COUNT)]


sparkle_update = partial(update_sparkle, lights)

try:
    pattern = getPattern()
    print(f"Using pattern {pattern['name']}.")
    start = time.time()
    lights.setPattern(pattern)
    lights.begin()
    chasing_timer = RepeatedTimer(lights.chasing, chasing_update)
    sparkle_timer = RepeatedTimer(SPARKLE_REFRESH, sparkle_update)
    while True:
        new_pattern = getPattern()
        if new_pattern != pattern:
            pattern = new_pattern
            lights.setPattern(new_pattern)
            start = time.time()
            chasing_timer.stop()
            sparkle_timer.stop()
            chasing_timer = RepeatedTimer(lights.chasing, update_chasing, lights)
            sparkle_timer = RepeatedTimer(SPARKLE_REFRESH, update_sparkle, lights)

        lights.setStrip()
        if lights.decibels:
            while not lights.q.empty():
                lights.buffer.append(lights.q.get())
            db = sum(lights.buffer) / len(lights.buffer) if lights.buffer else 0
            print(f"Decibels: {db:.2f} dB")
            try:
                lights.start_index = math.floor(
                    min((db / lights.decibels), 0.9999) * lights.num_starts
                )
            except:
                pass
        if lights.breathing > 0:
            lights.alpha = getAlpha(lights.breathing, time.time())
        lights.show()
except KeyboardInterrupt:
    lights.setPattern(off)
    lights.setStrip()
    lights.show()
    chasing_timer.stop()
    sparkle_timer.stop()
    time.sleep(0.1)
