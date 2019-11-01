#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time
import sys

color_scheme = 'RGBA'

OFF = 0
FIRE = 1
FADEOUT = 2


def cut_black_bg(image):
    width, height = image.size
    for y in range(height):
        for x in range(width):
            if image[x, y] == (255, 255, 255, 255):
                image[x, y] = (255, 255, 255, 0)
            if image[x, y][0] < 5 and image[x, y][1] < 5 and image[x, y][2] < 5:
                image[x, y] = (0, 0, 0, 0)


class SingleAnimation:
    def __init__(self, strip, image_src, duration_s, *fps):
        fps = fps or 25
        start_ms = time()
        self.brightness = 127 # 0-255
        self.width = strip['num']

        try:
            self.image = Image.open(image_src).convert(color_scheme)
        except Exception as e:
            print >> sys.stderr, ("image does not exist at" + image_src)
            print >> sys.stderr, "Exception: %s" % str(e)
            sys.exit(1)

        cut_black_bg(self.image)
        self.image = self.image.resize((strip['num'], duration_s * fps))

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=self.brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)


        self.active_row = [(0,0,0)] * self.width

        print("loaded in in {} ms".format(time() - start_ms))

    def move_to_next_frame(self):
        w, h = self.image.size()

        if h == 0:
            self.active_row = False
            return

        for i in range(self.width):
            try: 
                self.active_row[i] = self.image.getpixel((i, 0))
                if len(self.active_row[i]) == 4: # RGBA cleanup
                    print("rgba!")
                    r,g, b, a = self.active_row[i]
                    self.active_row[i] = (r, g, b)

            except Exception as err: 
                print(err)

        self.image = self.image.crop((0, 1, w, h))