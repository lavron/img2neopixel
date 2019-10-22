import neopixel
from img2neopixel import Animation
import time

PATH = "/home/pi/python/humax/"

image_src = PATH + "images/fire.jpg"
leds_pin = 18

leds_num = 25
max_brightness = 1
speed = 25  # rows per second
intencivity = 1  # new flame per second
# fps = 2
fps = 25
sleep_s = 1 / fps

strip = neopixel.NeoPixel(leds_pin,
                          leds_num,
                          brightness=max_brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)
animation = Animation(image_src, leds_num, max_brightness, speed, intencivity)


while True:
    time.sleep(sleep_s)

    animation.process()
    i = 0
    for led in animation.active_row:
        strip[i] = led
        i += 1
    strip.show()

