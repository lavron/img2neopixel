#!/usr/bin/env python

from animation import Animation
from random import randrange
import time
import board
import neopixel

image_src = "images/fire.jpg"
leds_pin = board.D18
leds_num = 25
max_brightness = 1.0
speed = 100 # y-pixels per second
intencivity =  1 # new flame per second
fps = 1
# fps = 25

leds = neopixel.NeoPixel(leds_pin, leds_num, brightness = max_brightness, auto_write=False, pixel_order = neopixel.GRB)


animation = Animation(image_src, leds_num, max_brightness, speed, intencivity)

frame_ms = 1 // fps

while True:
    animation.process()
    i = 0
    print(animation.active_row)
    for led in animation.active_row:
        # print("led: ", i, led)
        leds[i] = led
        i =+1
    leds.show()
    time.sleep(frame_ms)


