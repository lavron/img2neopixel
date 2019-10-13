#!/usr/bin/env python

from animation import Animation
from random import randrange
import time
import board
import neopixel


image_src = "images/fire2.jpg"
leds_pin = board.D18
leds_num = 25
max_brightness = 1.0
speed = 10 # rows per second 
intencivity = 1 # new flame per second
# fps = 2
fps = 25

leds = neopixel.NeoPixel(leds_pin, leds_num, brightness = max_brightness, auto_write=False, pixel_order = neopixel.GRB)


animation = Animation(image_src, leds_num, max_brightness, speed, intencivity)

sleep_s = 1 / fps

while True:
    # print("frame:", animation.active_row)
    animation.process()
    i = 0
    for led in animation.active_row:
        leds[i] = led
        i +=1
    leds.show()
    time.sleep(sleep_s)


