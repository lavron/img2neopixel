from img2neopixel import SingleAnimation
import time
import board



images_src = (
    '00.jpg',
    '01.jpg',
    '02.jpg',
    '03.jpg',
    '04.jpg',
)

strip = {
    'pin' : board.D18,
    'num' : 25
}

duration_s = 40

animation = SingleAnimation(strip, images_src, duration_s)

def process_animation():
    while animation.active:
        time.sleep(0.04) # == 25fps
        # time.sleep(1) # == 25fps
        animation.move_to_next_frame()

process_animation()