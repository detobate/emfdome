from decimal import *
import os

def pwm(pin, angle):
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/pi-blaster"
    os.system(cmd)


def set_rgb(pins, (r, g, b)):
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        r = str(Decimal(r) / 255)
        g = str(Decimal(g) / 255)
        b = str(Decimal(b) / 255)
        print('Red: %s Green: %s Blue: %s' % (r, g, b))
        pwm(pins['R'], r)
        pwm(pins['G'], g)
        pwm(pins['B'], b)
    else:
        print 'Invalid RGB value. RGB needs to be between 0 and 255'
