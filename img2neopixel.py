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
        start_ms = time.time()
        self.brightness = 127 # 0-255g

        try:
            self.image = Image.open(image_src).convert(color_scheme)
        except Exception as e:
            print ("Exception:", str(e))
            sys.exit(1)

        self.image = self.image.resize((strip['num'], duration_s * fps))

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=self.brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)

        self.active = True

        print("loaded in", (time.time() - start_ms), "ms")

    def move_to_next_frame(self):
        w, h = self.image.size()

        if h == 0:
            self.active = False
            return

        
        self.strip = [self.image.getpixel((i,0)) for i in range(self.image.size[0])]

        self.strip.show()
        