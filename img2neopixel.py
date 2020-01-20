#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time
import sys
import os


color_scheme = 'RGB'

class SingleAnimation:

    active_id = 0
    frame = 0
    state = True
    images = []
    
    def __init__(self, strip, images_src, duration_s, *fps):
        self.fps = fps or 25
        # fps = fps or 1
        self.duration_s = duration_s
        self.width = strip['num']
        self.height = duration_s * self.fps

        self.images_src = images_src

        for image_src in images_src:
            try:
                image = Image.open(image_src).convert(color_scheme)
                image = image.resize((self.width, self.height))
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                self.images.append(image) 
            except OSError as e:
                print ("Error:", str(e))

        self.images_count = len(self.images)

        if self.images_count == 0:
            print("no images")
            sys.exit(1)

        self.strip = neopixel.NeoPixel(strip['pin'],
                          strip['num'],
                          brightness=0.1,
                          auto_write=False)

        self.active_image = self.images[self.active_id]

        print("start image", self.images_src[self.active_id])
        # self.active_image.show()

    def clear_strip(self):
        self.strip.fill((0,0,0))
        self.strip.show()
    
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

    def set_image(self, _id):
        try:
            self.active_image = self.images[_id]
            self.active_id = _id
        except IndexError:
            print('no image', _id)

        self.frame = 0
        src = self.images_src[self.active_id]
        print(src)
        return src

    def next_image(self, direction = 1):
        
        self.active_id = direction + self.active_id

        if direction == 1 and self.active_id == self.images_count:
            self.active_id = 0

        if direction == -1 and self.active_id == 0:
            self.active_id = self.images_count - 1

        return os.path.basename(self.set_image(self.active_id))
    
    def move_to_next_frame(self):
        if self.frame == self.active_image.size[1]:
            # self.next_image() 
            self.frame = 0

        self.show_frame()
        self.frame +=1

    def show_frame(self):
        for i in range(self.width):
            self.strip[i] = self.active_image.getpixel((i,self.frame))

        self.strip.show()

