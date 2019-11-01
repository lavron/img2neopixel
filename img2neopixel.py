#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time
import sys
from machine import Pin

color_scheme = 'RGBA'

OFF = 0
FIRE = 1
FADEOUT = 2

class SingleAnimation:
    def __init__(self, strip, image_src, duration_s, *fps):
        fps = fps or 25
        start_ms = time.time()
        self.brightness = 127 # 0-255
        self.width = strip['num']

        try:
            self.image = Image.open(image_src).convert(color_scheme)
        except Exception as e:
            print ("Exception:", str(e))
            sys.exit(1)

        self.image = self.image.resize(Pin((strip['num']), duration_s * fps))

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=self.brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)

        pixel = (0,0,0,0) if color_scheme is 'RGBA' else (0,0,0)
        self.active_row = [pixel] * self.width

        print("loaded in in {} ms".format(time() - start_ms))

    def move_to_next_frame(self):
        w, h = self.image.size()

        if h == 0:
            self.active_row = False
            return

        for i in range(self.width):
            try: 
                self.active_row[i] = self.image.getpixel((i, 0))
                if color_scheme is 'RGBA': # RGBA -> RGB
                    r,g, b, a = self.active_row[i]
                    self.active_row[i] = (r, g, b)

            except Exception as err: 
                print(err)

        self.image = self.image.crop((0, 1, w, h))