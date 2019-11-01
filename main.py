from img2neopixel import SingleAnimation
import time
import os
import board

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)


strip = {
    'pin' : board.D18,
    'num' : 25
}
image_src = dname + "/images/fire.jpg"
duration_s = 10

animation = SingleAnimation(strip, image_src, duration_s)

frame = animation.active_row

while animation.active:
    time.sleep(0.04) # == 25fps
    animation.move_to_next_frame()