# Image To Neopixel

Python library for the animations on the Neopixels (WS2812 etc)
Initialy developed for the Fire animation.

## Idea

Create movie-like image with a trace of flame. Show it row-by-row on the LED strip.

![python's fire animation on the WS2812B strip](https://github.com/lavron/img2neopixel/blob/master/images/preview.gif)


## Getting Started

```python
animation = Animation("images/fire.jpg", leds_num)

while True:
    time.sleep(0.04) # 25 frames per second

    animation.process()
    for i, led in animation.active_row:
        strip[i] = led
    strip.show()

```

Check this video with Fire animation running on the WS2812B strip:
https://www.youtube.com/watch?v=rvxla5R7XIY


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details