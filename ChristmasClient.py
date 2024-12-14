import time

from utilities import getAlpha, getPattern

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

lights = ChristmasLights(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)


off = {
    "id": 1,
    "name": "Off",
    "pattern": ["#000000"],
    "active": True,
    "effects": {"breathing": 0, "chasing": 0, "sparkle": 0},
}


try:
    pattern = getPattern()
    print(f"Using pattern {pattern['name']}.")
    start = time.time()
    lights.setPattern(pattern)
    lights.begin()
    while True:
        new_pattern = getPattern()
        if new_pattern != pattern:
            pattern = new_pattern
            lights.setPattern(getPattern())
            start = time.time()
        lights.setStrip()
        if lights.chasing > 0:
            lights.pattern.insert(0, lights.pattern[-1])
            lights.pattern.pop(-1)
        if lights.breathing > 0:
            lights.alpha = getAlpha(lights.breathing, time.time())

        if lights.chasing:
            current = time.time() - start
            if (lights.chasing - (current % lights.chasing)) > 0.02:
                time.sleep(lights.chasing - (current % lights.chasing))
        if lights.sparkle:
            time.sleep(0.1)
        lights.show()
except KeyboardInterrupt:
    lights.setPattern(off)
    lights.setStrip()
    lights.show()
    time.sleep(0.1)
