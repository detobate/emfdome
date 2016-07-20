import colorsys, random, time

class Presets(object):
    """ Preset object class contains blocking loops for preset modes
        and should be threaded. Loops are killed by another thread setting leds.mode
        to None or a different mode """

    def __init__(self, leds):
        self.leds = leds

    def change(self, mode):
        if mode == 'strobe':
            self.leds.mode = 'strobe'
            while self.leds.mode == 'strobe':
                self.leds.set_rgb((0, 0, 0))
                # time.sleep(0.05)
                self.leds.set_rgb((255, 255, 255))
                # time.sleep(0.05)

        elif mode == 'randstrobe':
            self.leds.mode = 'randstrobe'
            while self.leds.mode == 'randstrobe':
                r = random.randrange(256)
                g = random.randrange(256)
                b = random.randrange(256)
                self.leds.set_rgb((0, 0, 0))
                time.sleep(0.01)
                self.leds.set_rgb((r, g, b))
                time.sleep(0.01)

        elif mode == 'police':
            self.leds.mode = 'police'
            while self.leds.mode == 'police':
                self.leds.set_rgb((255, 0, 0))
                time.sleep(0.25)
                self.leds.set_rgb((0, 0, 255))
                time.sleep(0.25)

        elif mode == 'random_colours':
            self.leds.mode = 'random_colours'
            while self.leds.mode == 'random_colours':
                r = random.randrange(256)
                g = random.randrange(256)
                b = random.randrange(256)
                self.leds.set_rgb((r, g, b))
                time.sleep(0.1)

        elif mode == 'fade':
            h = 0
            s = 1
            v = 255

            huestep = 0.005

            self.leds.mode = 'fade'
            while self.leds.mode == 'fade':
                (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
                self.leds.set_rgb((r, g, b))
                time.sleep(0.1)
                h = h + huestep
                if h >= 1:
                    h = 0

        elif mode == 'cycle':
            self.leds.mode = 'cycle'
            while self.leds.mode == 'cycle':
                self.leds.set_rgb((255, 0, 0))
                time.sleep(0.5)
                self.leds.set_rgb((255, 255, 0))
                time.sleep(0.5)
                self.leds.set_rgb((0, 255, 0))
                time.sleep(0.5)
                self.leds.set_rgb((0, 255, 255))
                time.sleep(0.5)
                self.leds.set_rgb((0, 0, 255))
                time.sleep(0.5)
                self.leds.set_rgb((255, 0, 255))
                time.sleep(0.5)


    ## What to do with this
    def fade_colour(self, (r1, g1, b1), (r2, g2, b2)):
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

        self.leds.mode = 'fade_colour'
        while self.leds.mode == 'fade_colour':
            print('Hue: %3f Saturation: %3f Value: %3f' % (h, s, v))
            (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
            self.leds.set_rgb((r, g, b))
            h = h + huestep
            step = step + 1
            if step > numsteps:
                step = 0
                huestep = huestep * -1
            time.sleep(0.05)
