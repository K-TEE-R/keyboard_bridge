#!/usr/bin/env python

import colorsys
import blinkt
import time
import threading

spacing = 360.0 / 16.0

class Rainbow:
    def __init__(self):
        self.offset = 0
        self.timer = threading.Timer(5, self.clear)
        blinkt.set_clear_on_exit()
        blinkt.set_brightness(0.1)
        
    def increment(self):
        self.timer.cancel()
        self.timer = threading.Timer(5, self.clear)
        self.timer.start()

        self.offset = self.offset + 1
        hue = 0
        num_pixels = 0
        if self.offset >= blinkt.NUM_PIXELS:
            num_pixels = blinkt.NUM_PIXELS
            hue = (self.offset * 20) % 360
        else:
            num_pixels = self.offset

        for x in range(num_pixels):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            blinkt.set_pixel(x, r, g, b)

        blinkt.show()

    def clear(self):
       blinkt.clear()
       blinkt.show()
       self.offset = 0
