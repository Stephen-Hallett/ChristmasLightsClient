from ChristmasLights import ChristmasLights
import time

# LED strip configuration:
LED_COUNT      = 100     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

lights = ChristmasLights(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
pattern = {"name": "Candy Cane",
               "pattern": ["#FFFFFF", "#ff2612"],
               "effects": {
                   "breathing": 0,
                   "chasing": 0.1,
                   "sparkle": 0
                }
            }
off = {"name": "Off",
               "pattern": ["#000000"],
               "effects": {
                   "breathing": 0,
                   "chasing": 0,
                   "sparkle": 0
                }
            }

try:
    lights.setPattern(pattern)
    lights.begin()

    while True:
        start = time.time()
        lights.setStrip()
        lights.pattern.insert(0, lights.pattern[-1])
        lights.pattern.pop(-1) 
        current = time.time()-start    
        if current < lights.chasing:
            time.sleep(lights.chasing - current)
        lights.show()
except KeyboardInterrupt:
    lights.setPattern(off)
    lights.setStrip()
    lights.show()
    time.sleep(0.1)

