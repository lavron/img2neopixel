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
        self.surface  = Image.new('RGB', self.image.size, (0,0,0))

        self.width, self.height = self.surface.size

        self.active_row = [(0,0,0)] * self.width
        self.ts =int(round(time.time() * 1000))
        self.frame_count = 0

        self.intencivity_max = int(intencivity * 1.5 * 1000)
        self.intencivity_min = int(intencivity * 0.5 * 1000)

        self.flame_next_in_ms = rand(self.intencivity_min, self.intencivity_max)
        self.flamed_ms = 0

    def add_image(self):

        self.flame_next_in_ms = rand(self.intencivity_min, self.intencivity_max)
        self.flamed_ms = 0

        min_width = self.surface.width // 5
        min_heigh = self.surface.height // 5

        width = rand(min_width, self.surface.width)
        heigh = rand(min_heigh, self.surface.height)
        size = (width, heigh)
        opacity = rand(1, int(self.brightness * 10)) / 10

        new_image =  self.image.copy().resize(size)

        xy = (rand(0, self.image.width - width), 0)

        self.surface.paste(new_image, xy)
    
        del new_image

        print("new image added")

    def process(self):
        self.frame_count +=1
        ts = time.time() * 1000
        elapsed_ms = int(ts - self.ts)
        move = round(elapsed_ms / self.row_ms)

        self.flamed_ms += elapsed_ms

        w, h = self.surface.size

        for i in range(self.width):
            self.active_row[i] = self.surface.getpixel((i, move))
            
        bg = Image.new('RGB', (w, h), (0,0,0))
        self.surface = self.surface.crop((0, move, w, h))
        bg.paste(self.surface, (0,0) )
        self.surface = bg

        if self.flamed_ms > self.flame_next_in_ms:
            self.add_image()
            
        del bg 
        self.ts = ts 