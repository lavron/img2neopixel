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

    active_image_id = 0
    frame = 0
    active = True
    images = []
    
    def __init__(self, strip, images_src, duration_s, *fps):
        fps = fps or 25
        # fps = fps or 1
        self.width = strip['num']
        self.height = duration_s * fps

        self.images_src = images_src

        for image_src in images_src:
            try:
                image = Image.open(root_dir + image_src).convert(color_scheme)
                image = image.resize((self.width, self.height))
                self.images.append(image) 
            except OSError as e:
                print ("Error:", str(e))

        self.images_count = len(self.images)

        if self.images_count == 0:
            print("no images")
            sys.exit(1)

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=0.5,
                          auto_write=False)

        self.active_image = self.images[self.active_image_id]

        print("img2neopixel boot finished")

    def on(self):
        self.active = True

    def off(self):
        self.active = False
    
    def brightness_set(self, brightness):
        self.strip.brightness = min (1, max(0, brightness))

    def brightness_plus(self):
        if self.strip.brightness < 1:
           self.strip.brightness =+ 0.1

    def brightness_minus(self):
        if self.strip.brightness > 0:
            self.strip.brightness =- 0.1

    def faster():
        pass
    def slower():
        pass

    def set_image(self, image_id):
        try:
            self.active_image_id = self.images[image_id]
        except IndexError:
            print('sorry, no image', image_id)

    def prev_image(self):
        self.active_image_id -=1
        if self.active_image_id == 0:
            self.active_image_id = self.images_count
        self.frame = 0
        self.active_image = self.images[self.active_image_id]

    def next_image(self):
        self.active_image_id +=1
        if self.active_image_id == self.images_count:
            self.active_image_id = 0
        self.frame = 0
        self.active_image = self.images[self.active_image_id]
        
        print("start image", self.images_src[self.active_image_id])
    
    def move_to_next_frame(self):
        if self.frame == self.active_image.size[1]:
            self.next_image()

        self.show_frame()
        self.frame +=1

    def show_frame(self):
        for i in range(self.width):
            self.strip[i] = self.active_image.getpixel((i,self.frame))

        self.strip.show()

