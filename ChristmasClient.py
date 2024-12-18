import asyncio
import math
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

SPARKLE_REFRESH = 4


async def update_chasing(lights: ChristmasLights):
    while True:
        if lights.chasing > 0:
            lights.pattern = lights.pattern[-1:] + lights.pattern[:-1]
        await asyncio.sleep(lights.chasing)


async def update_sparkle(lights: ChristmasLights):
    while True:
        if lights.sparkle > 0:
            lights.active = [i for i in range(LED_COUNT) if lights.getSparkle()]
        await asyncio.sleep(SPARKLE_REFRESH)


async def main():
    lights = ChristmasLights(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )

    off = {
        "id": 1,
        "name": "Off",
        "pattern": ["#000000"],
        "active": True,
        "effects": {"breathing": 0, "chasing": 0, "sparkle": 0, "decibels": 0},
    }

    try:
        pattern = getPattern()
        print(f"Using pattern {pattern['name']}.")
        lights.setPattern(pattern)
        lights.begin()

        chasing_task = asyncio.create_task(update_chasing(lights))
        sparkle_task = asyncio.create_task(update_sparkle(lights))
        while True:
            new_pattern = getPattern()
            if new_pattern != pattern:
                pattern = new_pattern
                lights.setPattern(new_pattern)

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
                except Exception as e:
                    print(f"Error updating start index: {e}")

            if lights.breathing > 0:
                lights.alpha = getAlpha(lights.breathing, time.time())
            lights.show()
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        lights.setPattern(off)
        lights.setStrip()
        lights.show()
        chasing_task.cancel()
        sparkle_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
