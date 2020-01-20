from img2neopixel import SingleAnimation
import time
import board
import os



images_src = [
    # 'curiosity.jpg',
    'sunrise01.jpg',
    'sunset01.jpg',
    '00.jpg',
    '01.jpg',
    '03.jpg',
    '13.jpg',
    '14.jpg',
    '21.jpg',
    '22.jpg',
    '24.jpg',
    '25.jpg',
    '26.jpg',
    '27.jpg',
]

strip = {
    'pin' : board.D18,
    'num' : 112
}

duration_s = 20

abspath = os.path.abspath(__file__)
root_dir = os.path.dirname(abspath) + "/images/"

for i, src in enumerate(images_src): 
    images_src[i] = root_dir + images_src[i]


animation = SingleAnimation(strip, images_src, duration_s)
animation.state = True

animation.clear_strip()


def process_animation():
    while True:
        time.sleep(0.04) # == 25fps
        animation.move_to_next_frame()

process_animation()