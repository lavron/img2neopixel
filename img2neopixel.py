#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time

color_scheme = 'RGBA'


class Animation:
    def __init__(self, image_src, leds_num, brightness, speed, intencivity):

        self.brightness = brightness

        self.row_ms = 1000 / speed
        
        self.image = Image.open(image_src).convert(color_scheme)
        
        width, height = self.image.size
        proportion = height / width

        self.image = self.image.resize((leds_num, int(leds_num * proportion)))
        width, height = self.image.size


        self.surface  = Image.new(color_scheme, (width, height * 10), (0,0,0))
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
        min_heigh = self.surface.height // 20

        width = rand(min_width, self.surface.width)
        heigh = rand(min_heigh, self.surface.height)
        size = (width, heigh)
        opacity = rand(63, int(self.brightness * 255)) 
        new_image =  self.image.copy().resize(size)
        new_image.putalpha(opacity)
        xy = (rand(0, self.image.width - width), 0)

        bg = Image.new(color_scheme, self.surface.size, (0,0,0,0))
        bg.paste(self.surface, (0,0))
        bg.paste(new_image, xy, mask=new_image)


        self.surface = bg

        # self._screenshot(self.surface, 'after_op=' + str(opacity))
    
        del new_image, bg

    def _screenshot(self, image, suffix = ''):
        if suffix is not '':
            suffix ="_" + suffix
        filename = "new_img_" + str(self.frame_count) + suffix
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

        self._screenshot(self.surface, '__before' +  str(self.surface.size))
        self.surface = self.surface.crop((0, move, w, h))
        self._screenshot(self.surface, '_after' + str(self.surface.size) + str(move))
        # self._screenshot(bg)

        bg.paste(self.surface, (0,0) )
        self.surface = bg

        if self.flamed_ms > self.flame_next_in_ms:
            self.add_image()
            
        del bg 
        self.ts = ts 