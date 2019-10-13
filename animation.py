#!/usr/bin/env python

from random import randrange
import neopixel
import datetime
from PIL import Image



def one_chance_from(value):
    return 1 == randrange(1, value)


class Animation:
    def __init__(self, image_src, leds_num, brightness, speed, intencivity):

        self.brightness = brightness
        self.speed = speed / 1000 # rows per ms
        self.intencivity = intencivity * 1000 # new flame per ms
        
        self.image = Image.open(image_src)   
        
        width, height = self.image.size
        proportion = height / width
        
        self.image = self.image.resize((leds_num, int(leds_num * proportion)))
             
        self.width, self.height = self.image.size
        
        self.active_row = [(0,0,0)] * self.width
        
        self.start_ms = datetime.datetime.now() 
        self.now_ms =  self.start_ms

    

    def add_image(self):
        min_width = self.image.width // 5
        min_heigh = self.image.height // 5

        width = randrange(min_width, self.image.width)
        heigh = randrange(min_heigh, self.image.height)
        opacity = randrange(1, int(self.brightness * 10)) / 10

        new_image = Image(self.image).resize(width, heigh)

        x = randrange(0, self.image.width - width)
        y = 0
        self.image = Image.blend(self.image, new_image, alpha=opacity)
        
        del new_image

    def process(self):
        elapsed = datetime.datetime.now()  - self.start_ms 
        
        move = self.height * ((elapsed.microseconds * 1000) % self.speed) 

        
        for i in range(self.width):
            self.active_row[i] =  self.image.getpixel((i, move))
            
        
        bg = Image.new('RGBA', (self.image.size), (0,0,0))
        
        bg.paste(self.image, (0,0) )
        
        if one_chance_from(self.intencivity):
            self.add_image()
            
        del bg  