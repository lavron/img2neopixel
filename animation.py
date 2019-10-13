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
        # self.image_src = image_src
        self.speed = speed / 1000 # rows per ms
        
        self.intencivity = intencivity * 1000 # new flame per ms
        
        self.image = Image.open(image_src)   
        
        width, height = self.image.size
        proportion = height / width

        self.image = self.image.resize((leds_num, int(leds_num * proportion)))
        self.width, self.height = self.image.size

        self.active_row = [(0,0,0)] * self.width
        
        self.ts =int(round(time.time() * 1000))

        self.frame_count = 0

    

    def add_image(self):
        min_width = self.image.width // 5
        min_heigh = self.image.height // 5

        width = rand(min_width, self.image.width)
        heigh = rand(min_heigh, self.image.height)
        size = (width, heigh)
        opacity = rand(1, int(self.brightness * 10)) / 10

        new_image =  self.image.copy()
        new_image = new_image.resize(size)

        xy = (rand(0, self.image.width - width), 0)
        self.image.paste(new_image, xy, new_image.convert('RGB'))

        print("new image created")

        new_image.show()
    
        del new_image

    def process(self):
        self.frame_count +=1
        ts = time.time() * 1000
        elapsed = int(ts - self.ts)
        offset = elapsed  % (self.speed * 1000) / (self.speed * 1000)
        move = self.height * offset

        w, h = self.image.size

        print("offset:", offset)
        print("elapsed:", elapsed)
        print("move:", move)
        print()

        for i in range(self.width):
            self.active_row[i] =  self.image.getpixel((i, move))
            
        bg = Image.new('RGB', (w, h), (0,0,0))

        
        self.image.crop((0, 30, w, h))
        
        bg.paste(self.image, (0,0) )

        self.image = bg
        
        if one_chance_from(self.intencivity):
            self.add_image()
            
        del bg 
        self.ts = ts 