import neopixel
from img2neopixel import Animation
import time

image_src = "images/fire.jpg"

<<<<<<< HEAD
image_src = "images/fire2.jpg"
# image_src = "images/amoled-4.jpg"
# image_src = "images/Fire-Wallpaper-HD.jpg"
strip_pin = board.D18

strip_num = 25
max_brightness = 0.5
speed = 25 # rows per second 
intencivity = 1 # new flame per second
# fps = 2
=======
leds_pin = 18
leds_num = 25

max_brightness = 1
speed = 25  # rows per second, tuning purposes
intencivity = 1  # new flame per second, tuning purposes
>>>>>>> 009eaf5bb299a2070dfa23c226e7362faaa84e11
fps = 25

strip = neopixel.NeoPixel(leds_pin,
                          leds_num,
                          brightness=max_brightness,
                          auto_write=False,
                          pixel_order=neopixel.GRB)

<<<<<<< HEAD
strip = neopixel.NeoPixel(strip_pin, strip_num, brightness = max_brightness, auto_write=False, pixel_order = neopixel.GRB)
animation = Animation(image_src, strip_num, max_brightness, speed, intencivity)
=======
animation = Animation(image_src, leds_num, max_brightness, speed, intencivity)
>>>>>>> 009eaf5bb299a2070dfa23c226e7362faaa84e11

sleep_s = 1 / fps

while True:
    time.sleep(sleep_s)

    animation.process()
<<<<<<< HEAD
    i = 0
    # print("animation.active_row:", animation.active_row)
    for led in animation.active_row:
        strip[i] = led
        i +=1
=======
    for i, led in animation.active_row:
        strip[i] = led
>>>>>>> 009eaf5bb299a2070dfa23c226e7362faaa84e11
    strip.show()

