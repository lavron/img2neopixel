#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time
import sys

color_scheme = 'RGB'

OFF = 0
FIRE = 1
FADEOUT = 2

class SingleAnimation:
    def __init__(self, strip, image_src, duration_s, *fps):
        fps = fps or 25
        self.frame = 0
        self.brightness = 127 # 0-255g
        self.width = strip['num']
        self.height = duration_s * fps

        self.image_src = image_src

        try:
            self.image = Image.open(image_src).convert(color_scheme)
        except Exception as e:
            print ("Exception:", str(e))
            sys.exit(1)
        self.image = self.image.resize((self.width, self.height))

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=self.brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)

        self.active = True

    def move_to_next_frame(self):

        if self.frame == self.image.size[1]:
            self.frame = 0
            print("restart image")

        for i in range(self.width):
            self.strip[i] = self.image.getpixel((i,self.frame))

        self.strip.show()

        self.frame +=1
        