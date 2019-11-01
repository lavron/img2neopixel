from img2neopixel import Animation, SingleAnimation
import time
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)


strip = {
    'pin' : 18,
    'num' : 25
}
image_src = dname + "images/fire.jpg"
duration_s = 10

animation = SingleAnimation(strip, image_src, duration_s)

frame = animation.active_row

while frame:
    time.sleep(0.04) # == 25fps

    for i, led in frame:
        strip[i] = led

    strip.show()
    animation.move_to_next_frame()

