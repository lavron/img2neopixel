import neopixel
from img2neopixel import Animation
import time

image_src = "images/fire.jpg"

leds_pin = 18
leds_num = 25

max_brightness = 1
speed = 25  # rows per second, tuning purposes
intencivity = 1  # new flame per second, tuning purposes
fps = 25

strip = neopixel.NeoPixel(leds_pin,
                          leds_num,
                          brightness=max_brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)

animation = Animation(image_src, leds_num, max_brightness, speed, intencivity)

sleep_s = 1 / fps

while True:
    time.sleep(sleep_s)

    animation.process()
    for i, led in animation.active_row:
        strip[i] = led
    strip.show()

