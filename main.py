#!/usr/bin/env python

from img2neopixel import Animation
import time
import board
import neopixel


image_src = "images/fire2.jpg"
# image_src = "images/fire2-transparent.png"
leds_pin = board.D18

leds_num = 25
max_brightness = 0.5
speed = 25 # rows per second 
intencivity = 1 # new flame per second
# fps = 2
fps = 25
sleep_s = 1 / fps


leds = neopixel.NeoPixel(leds_pin, leds_num, brightness = max_brightness, auto_write=False, pixel_order = neopixel.GRB)
animation = Animation(image_src, leds_num, max_brightness, speed, intencivity)


while True:
    animation.process()
    i = 0
    for led in animation.active_row:
        leds[i] = led
        i +=1
    leds.show()
    time.sleep(sleep_s)


