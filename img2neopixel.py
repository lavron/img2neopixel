#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time
import sys
import os


color_scheme = 'RGB'

abspath = os.path.abspath(__file__)
root_dir = os.path.dirname(abspath) + "/images/"

OFF = 0
FIRE = 1
FADEOUT = 2

class SingleAnimation:
    def __init__(self, strip, images_src, duration_s, *fps):
        fps = fps or 25
        # fps = fps or 1
        self.frame = 0
        self.brightness = 127 # 0-255g
        self.width = strip['num']
        self.height = duration_s * fps

        self.images_src = images_src
        self.images = []

        for image_src in images_src:
            try:
                image = Image.open(root_dir + image_src).convert(color_scheme)
                image = image.resize((self.width, self.height))
                # image.save(root_dir + "resized_" + image_src)
                self.images.append(image) 

            except OSError as e:
                print ("Error:", str(e))

        self.images_count = len(self.images)

        if self.images_count == 0:
            print("no images")
            sys.exit(1)

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=self.brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)


        self.active_image_id = 0
        self.active_image = self.images[self.active_image_id]

        self.active = True

        print("boot finished")

    def move_to_next_frame(self):

        if self.frame == self.active_image.size[1]:
            self.active_image_id +=1
            if self.active_image_id == self.images_count:
                self.active_image_id = 0
            self.frame = 0
            self.active_image = self.images[self.active_image_id]
            print("start image", self.images_src[self.active_image_id])

        for i in range(self.width):
            self.strip[i] = self.active_image.getpixel((i,self.frame))

        self.strip.show()

        self.frame +=1