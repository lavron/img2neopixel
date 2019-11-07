from img2neopixel import SingleAnimation
import time
import board
import os



# images_src = (
#     '00.jpg',
#     '01.jpg',
#     '02.jpg',
#     '03.jpg',
#     '04.jpg',
# )

# images_src = (
#     '11.jpg',
#     '12.jpg',
#     '13.jpg',
#     '14.jpg',
#     '15.jpg',
#     '16.jpg',
# )
# images_src = (
#     '27.jpg',

#     '20.jpg',
#     '21.jpg',
#     '22.jpg',
#     '23.jpg',
#     '24.jpg',
#     '25.jpg',
#     '26.jpg',
# )

strip = {
    'pin' : board.D18,
    'num' : 25
}

duration_s = 40

abspath = os.path.abspath(__file__)
root_dir = os.path.dirname(abspath) + "/images/"

images_src = []
# r=root, d=directories, f = files
for r, d, f in os.walk(root_dir):
    for file in f:
        if '.jpg' in file:
            images_src.append(os.path.join(r, file))

animation = SingleAnimation(strip, images_src, duration_s)

def process_animation():
    while animation.active:
        time.sleep(0.04) # == 25fps
        # time.sleep(1) # == 25fps
        animation.move_to_next_frame()

process_animation()