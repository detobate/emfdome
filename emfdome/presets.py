import colorsys, random, time
from .common import *

def fade_colour(pins, queue, (r1, g1, b1), (r2, g2, b2)):
    (h1, s1, v1) = colorsys.rgb_to_hsv(r1, g1, b1)
    (h2, s2, v2) = colorsys.rgb_to_hsv(r2, g2, b2)

    print('Start Hue: %3f Saturation: %3f Value: %3f' % (h1, s1, v1))
    print('End   Hue: %3f Saturation: %3f Value: %3f' % (h2, s2, v2))

    numsteps = 80
    huestep = (h2 - h1) / numsteps

    h = h1
    s = s1
    v = v1
    step = 0

    while queue.empty():
        print('Hue: %3f Saturation: %3f Value: %3f' % (h, s, v))
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        set_rgb(pins, (r, g, b))
        h = h + huestep
        step = step + 1
        if step > numsteps:
            step = 0
            huestep = huestep * -1
        time.sleep(0.05)


def strobe(pins, queue):
    while queue.empty():
        set_rgb(pins, (0, 0, 0))
        # time.sleep(0.05)
        set_rgb(pins, (255, 255, 255))
        # time.sleep(0.05)

def randstrobe(pins, queue):
    while queue.empty():
        r = random.randrange(256)
        g = random.randrange(256)
        b = random.randrange(256)
        set_rgb(pins, (0, 0, 0))
        time.sleep(0.01)
        set_rgb(pins, (r, g, b))
        time.sleep(0.01)


def police(pins, queue):
    while queue.empty():
        set_rgb(pins, (255, 0, 0))
        time.sleep(0.25)
        set_rgb(pins, (0, 0, 255))
        time.sleep(0.25)


def random_colours(pins, queue):
    while queue.empty():
        r = random.randrange(256)
        g = random.randrange(256)
        b = random.randrange(256)
        set_rgb(pins, (r, g, b))
        time.sleep(0.1)


def fade_all(pins, queue):
    h = 0
    s = 1
    v = 255

    huestep = 0.005

    while queue.empty():
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        set_rgb(pins, (r, g, b))
        time.sleep(0.1)
        h = h + huestep
        if h >= 1:
            h = 0


def cycle(pins, queue):
    while queue.empty():
        set_rgb(pins, (255, 0, 0))
        time.sleep(0.5)
        set_rgb(pins, (255, 255, 0))
        time.sleep(0.5)
        set_rgb(pins, (0, 255, 0))
        time.sleep(0.5)
        set_rgb(pins, (0, 255, 255))
        time.sleep(0.5)
        set_rgb(pins, (0, 0, 255))
        time.sleep(0.5)
        set_rgb(pins, (255, 0, 255))
        time.sleep(0.5)
