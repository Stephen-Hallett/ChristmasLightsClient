import argparse
import time

from rpi_ws281x import Color, PixelStrip

# LED strip configuration:
LED_COUNT = 100  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

"""Looks like the process is to do strip[i] = Color(r,g,b), then do strip.show() to update."""


def hex2rgb(hexcode: str) -> tuple[int, int, int]:
    code = hexcode.lstrip("#")
    return tuple(int(code[i : i + 2], 16) for i in (0, 2, 4))


# Main program logic follows:
if __name__ == "__main__":
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--clear", action="store_true", help="clear the display on exit"
    )
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )
    # Intialize the library (must be called once before other functions).
    strip.begin()

    pattern = {
        "name": "Candy Cane",
        "pattern": ["#FFFFFF", "#ff2612"],
        "effects": {"breathing": 0, "chasing": 0.5, "sparkle": 1},
    }

    for i in range(strip.numPixels()):
        strip[i] = Color(255, 255, 255)
    strip.show()
    time.sleep(2)
    # for i in range(strip.numPixels()):
    #    strip[i] = Color(0,0,255)
    # strip.show()
    # time.sleep(2)
    # for i in range(strip.numPixels()):
    #    strip[i] = Color(0,0,0)
    # strip.show()
    for i in range(200, -1, -50):
        strip.setBrightness(i)
        strip.show()
        time.sleep(2)
