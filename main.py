from img2neopixel import Animation, SingleAnimation
import time

image_src = "images/fire.jpg"

strip = {
    'pin' : 18,
    'num' : 25
}
   


brightness = 127 # 0-255

# animation = Animation(strip, image_src, max_brightness)

duration_s = 10

single_animation = SingleAnimation(strip, image_src, duration_s, brightness)

while True:
    time.sleep(0.04) # == 25fps

    animation.process()
    for i, led in animation.active_row:
        strip[i] = led

    strip.show()

