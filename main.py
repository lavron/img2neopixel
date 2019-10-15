#!/usr/bin/env python

from img2neopixel import Animation
import time
import board
import neopixel


image_src = "images/fire2.jpg"
# image_src = "images/amoled-4.jpg"
# image_src = "images/Fire-Wallpaper-HD.jpg"
strip_pin = board.D18

strip_num = 25
max_brightness = 0.5
speed = 25 # rows per second 
intencivity = 1 # new flame per second
# fps = 2
fps = 25
sleep_s = 1 / fps


strip = neopixel.NeoPixel(strip_pin, strip_num, brightness = max_brightness, auto_write=False, pixel_order = neopixel.GRB)
animation = Animation(image_src, strip_num, max_brightness, speed, intencivity)


while True:
    time.sleep(sleep_s)

    animation.process()
    i = 0
    # print("animation.active_row:", animation.active_row)
    for led in animation.active_row:
        strip[i] = led
        i +=1
    strip.show()

