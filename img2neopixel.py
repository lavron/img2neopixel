#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time

import numpy as np

color_scheme = 'RGBA'


class Animation:
    def __init__(self, image_src, leds_num, brightness, speed, intencivity):

        self.brightness = brightness

        self.row_ms = 1000 / speed
        
        self.image = Image.open(image_src).convert(color_scheme)
        width, height = self.image.size
        proportion = height / width


        self.image = self.image.resize((leds_num, int(leds_num * proportion * 10)))
        width, height = self.image.size



        pixdata =  self.image.load()
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)
                if pixdata[x, y][0] < 5 and pixdata[x, y][1] < 5 and pixdata[x, y][2] < 5:
                    pixdata[x, y] = (0, 0, 0, 0)

        self.surface  = Image.new(color_scheme, (width, height), (0,0,0,0))
        self.width, self.height = self.surface.size

        self.active_row = [(0,0,0)] * self.width
        self.ts =int(round(time.time() * 1000))
        self.frame_count = 0

        self.intencivity_max = int(1/intencivity * 1.5 * 1000)
        self.intencivity_min = int(1/intencivity * 0.5 * 1000)

        self.flame_next_in_ms = rand(self.intencivity_min, self.intencivity_max)
        self.flamed_ms = 0

    def add_image(self):

        self.flame_next_in_ms = rand(self.intencivity_min, self.intencivity_max)
        self.flamed_ms = 0

        min_width = self.surface.width // 4
        min_height = self.surface.height // 10

        width = rand(min_width, self.surface.width)
        height = rand(min_height, self.surface.height)
        size = (width, height)
        opacity = rand(63, int(self.brightness * 255)) 
        new_image =  self.image.copy().resize(size)
        
        # xy = (rand(0, self.surface.width - width), rand(0, self.surface.height - height))
        xy = (rand(0, self.surface.width - width), 0)

        bg = Image.new(color_scheme, self.surface.size, (0,0,0,0))
        bg.paste(self.surface, (0,0))
        bg.paste(new_image, xy, mask=new_image)

        self.surface = bg
        self._screenshot(self.surface)
        del new_image, bg

    def _screenshot(self, image, suffix = ''):
        if suffix is not '':
            suffix ="_" + suffix
        filename = "img_"  + suffix + str(self.frame_count)
        if color_scheme == 'RGBA':
            format = "PNG"
            filename +=  ".png"
        else:
            filename +=".jpg"
            format = "JPEG"
        image.save("images/tmp/" + filename, format=format)

    def process(self):
        self.frame_count +=1
        ts = time.time() * 1000
        elapsed_ms = int(ts - self.ts)
        move = round(elapsed_ms / self.row_ms)

        self.flamed_ms += elapsed_ms

        w, h = self.surface.size

        for i in range(self.width):
            try: 
                self.active_row[i] = self.surface.getpixel((i, move))
                if len(self.active_row[i]) == 4:
                    r,g, b, a = self.active_row[i]
                    self.active_row[i] = (r, g, b)

            except Exception as err: 
                print(err)
                print("i, move", i, move)
            
        bg = Image.new(color_scheme, (w, h), (0,0,0,0))

        self.surface = self.surface.crop((0, move, w, h))

        bg.paste(self.surface, (0,0) )
        self.surface = bg


        if self.flamed_ms > self.flame_next_in_ms:
            self.add_image()
            
        del bg 
        self.ts = ts 