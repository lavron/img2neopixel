#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time

color_scheme = 'RGBA'

OFF = 0
FIRE = 1
FADEOUT = 2


class SingleAnimation:
    def __init__(self, strip, image_src, duration_s, *brightness):
        start_ms = time()
        self.brightness = brightness or 127

        self.image = Image.open(image_src).convert(color_scheme)
        self.image = self.image.resize((strip['num'], int(strip['num'] )))


class Animation:

    def __init__(self, leds_pin, leds_num, image_src, *brightness):

        start_ms = time()

        self.brightness = brightness or 127

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

        self.ms_from, self.ms_to = int(1/intencivity * 0.5 * 1000), int(1/intencivity * 1.5 * 1000)

        self._set_next_flame_time()

        self.state = FIRE

        print("loaded in in {} ms {:06d}\n".format(time() - start_ms))

        
    def _set_next_flame_time(self):
        self.flame_next_in_ms = rand(self.ms_from, self.ms_to)
        self.flamed_ms = 0

    def _add_flame(self):

        width = rand(self.surface.width // 3, self.surface.width)
        height = rand(self.surface.height // 10, self.surface.height)
        size = (width, height)
        opacity = rand(63, int(self.brightness)) 
        new_image =  self.image.copy().resize(size)
    

        bg = Image.new(color_scheme, self.surface.size, (0,0,0,0))
        bg.paste(self.surface, (0,0))
        bg.paste(new_image, (rand(0, self.surface.width - width), 0), mask=new_image)

        self.surface = bg
        del new_image, bg

        self._set_next_flame_time()

    def process(self):
            
        self.frame_count +=1
        ts = time.time() * 1000
        elapsed_ms = int(ts - self.ts)
        if self.state == FADEOUT:
            elapsed_ms = elapsed_ms *5

        move = elapsed_ms // 0.04

        self.flamed_ms += elapsed_ms

        w, h = self.surface.size

        if h <= move: # fadeout is finished
            self.state = OFF
            self.surface  = Image.new(color_scheme, self.image.size, (0,0,0,0))
            return 

        for i in range(self.width):
            try: 
                self.active_row[i] = self.surface.getpixel((i, move))
                if len(self.active_row[i]) == 4:
                    r,g, b, a = self.active_row[i]
                    self.active_row[i] = (r, g, b)

            except Exception as err: 
                print(err)
                print("i, move:", i, move)
            

        self.surface = self.surface.crop((0, move, w, h))
        self.ts = ts 

        if self.state == FADEOUT:
            return

        bg = Image.new(color_scheme, (w, h), (0,0,0,0))
        bg.paste(self.surface, (0,0) )
        self.surface = bg
        del bg 
        
        if self.flamed_ms > self.flame_next_in_ms:
            self._add_flame()
    

    def _screenshot(self, image, suffix = ''):
        if suffix is not '':
            suffix ="_" + suffix
        # filename = "img_"  + suffix + str(self.frame_count)
        filename = "img_"
        if color_scheme == 'RGBA':
            format = "PNG"
            filename +=  ".png"
        else:
            filename +=".jpg"
            format = "JPEG"
        image.save("images/tmp/" + filename, format=format)