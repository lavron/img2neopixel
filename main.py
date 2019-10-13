#!/usr/bin/env python

from animation import Animation
from random import randrange
import time
import board

image = "images/fire.jpg"
leds_pin = board.D18
leds_num = 25
max_brightness = 1.0
speed = 100 # y-pixels per second
intencivity =  1 # new flame per second
fps = 25

leds = neopixel.NeoPixel(leds_pin, leds_num, brightness = max_brightness, auto_write=False, pixel_order = neopixel.GRB)

animation = Animation(image, leds_num, max_brightness, speed, intencivity)

frame_ms = 1000 // fps

while True:
    animation.process()
    for i, led in animation.active_row:
        leds[i] = led
    leds.show()
    time.sleep(frame_ms)



