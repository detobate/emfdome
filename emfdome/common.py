from decimal import *
import os, threading

class LightStrip(object):

    def __init__(self, pins):
        self.pins = pins
        self.mode = None

    def pwm(self, pin, angle):
        cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/pi-blaster"
        os.system(cmd)

    def set_rgb(self, (r, g, b)):
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            r = str(Decimal(r) / 255)
            g = str(Decimal(g) / 255)
            b = str(Decimal(b) / 255)
            print('Red: %s Green: %s Blue: %s' % (r, g, b))
            self.pwm(self.pins['R'], r)
            self.pwm(self.pins['G'], g)
            self.pwm(self.pins['B'], b)
        else:
            print 'Invalid RGB value. RGB needs to be between 0 and 255'




