#!/usr/bin/env python

from random import randrange as rand
import neopixel
import datetime
from PIL import Image
import time



def one_chance_from(value):
    return 1 == rand(1, value)


class Animation:
    def __init__(self, image_src, leds_num, brightness, speed, intencivity):

        self.brightness = brightness

        self.row_ms = 1000 / speed
        
        self.image = Image.open(image_src).convert('RGB')
        
        width, height = self.image.size
        proportion = height / width

        self.image = self.image.resize((leds_num, int(leds_num * proportion)))
        width, height = self.image.size


        self.surface  = Image.new('RGB', (width, height * 10), (0,0,0))
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
        opacity = rand(1, int(self.brightness * 10)) / 10

        new_image =  self.image.copy().resize(size)
        bg = Image.new('RGB', self.surface.size, (0,0,0))
        xy = (rand(0, self.image.width - width), 0)
        bg.paste(new_image, xy)

        self.surface = Image.blend(self.surface, bg, opacity)

        # filename = "new_img_" + str(self.frame_count) + ".jpg"
        # self.surface.save("images/tmp/" + filename, format="JPEG")
    
        del new_image

        # print("new image added")

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
            except Exception as err: 
                print(err)
                print("i, move", i, move)
            
        bg = Image.new('RGB', (w, h), (0,0,0))
        self.surface = self.surface.crop((0, move, w, h))
        bg.paste(self.surface, (0,0) )
        self.surface = bg

        if self.flamed_ms > self.flame_next_in_ms:
            self.add_image()
            
        del bg 
        self.ts = ts 