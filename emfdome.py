#!/usr/bin/python

from twython import Twython
from twython import TwythonStreamer
from decimal import *
import time
import os
import webcolors
import re
import sys
import colorsys
import threading
import random
 
STEP = 100
DELAY = 0.5

# Twitter Keys
APP_KEY = ''
APP_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

# servo to pin mapping
#R = '4'
#G = '17'
#B = '18'
R = '18'
G = '23'
B = '24'

# Keyword
WATCH = '@emfdome'

mode = '#ffffff'

def pwm(pin, angle):
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/pi-blaster"
    os.system(cmd)
    #time.sleep(DELAY)

def test_tweet(thing):
    try: 
        float(thing)
        return thing
    except ValueError: 
        pass

def parse_colour(tweet):
    parts = tweet.lower().split(" ")
    for i in range(len(parts)):
        if parts[i] == 'fade':
            return 'fade'
        elif parts[i] == 'random':
            return 'random'
        elif parts[i] == 'randstrobe':
            return 'randstrobe'
        elif parts[i] == 'strobe':
            return 'strobe'
        elif parts[i] == 'police':
            return 'police'
        elif re.search('^#', parts[i]):
            return parts[i]

    m = re.search('(\d+ \d+ \d+)', tweet.lower())
    if m:
        return m.group(0)

def set_colour(tweet):
    r = None
    g = None
    b = None
    foo = tweet.split(" ")
    for i in range(len(foo)):
        if re.search('^#', foo[i]):
            try:
                value = webcolors.hex_to_rgb(foo[i])
                r = value[0]
                g = value[1]
                b = value[2]
            except: 
                print foo[i] + ' is not a webcolor'
                pass
        else:
            value = test_tweet(foo[i])
            if value is not None:
                if r is None:
                    r = int(value)
                elif g is None:
                    g = int(value)
                elif b is None:
                    b = int(value)
    set_rgb((r, g, b))
    
def set_rgb((r, g, b)):
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        r = str(Decimal(r) / 255)
        g = str(Decimal(g) / 255)
        b = str(Decimal(b) / 255)
        print 'Red: %s Green: %s Blue: %s' % (r, g, b)
        pwm(R, r)
        pwm(G, g)
        pwm(B, b)
        #twitter.update_status(status='Dome set to Red:"%s" Green:"%s" Blue:"%s"' % (r,g,b)) 
    else:
        print 'Invalid RGB value. RGB needs to be between 0 and 255'


def fade_colour((r1, g1, b1), (r2, g2, b2)):

    (h1, s1, v1) = colorsys.rgb_to_hsv(r1, g1, b1)
    (h2, s2, v2) = colorsys.rgb_to_hsv(r2, g2, b2)

    print 'Start Hue: %3f Saturation: %3f Value: %3f' % (h1, s1, v1)
    print 'End   Hue: %3f Saturation: %3f Value: %3f' % (h2, s2, v2)

    numsteps = 80
    huestep = (h2 - h1) / numsteps

    h = h1
    s = s1
    v = v1
    step = 0

    while True:
        print 'Hue: %3f Saturation: %3f Value: %3f' % (h, s, v)
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        set_rgb((r, g, b))
        h = h + huestep
        step = step + 1
        if step > numsteps:
            step = 0
            huestep = huestep * -1
        time.sleep(0.05)

def strobe():
    while mode == 'strobe':
        set_rgb((0, 0, 0))
        #time.sleep(0.05)
        set_rgb((255, 255, 255))
        #time.sleep(0.05)

def randstrobe():
    while mode == 'randstrobe':
        r = random.randrange(256)
        g = random.randrange(256)
        b = random.randrange(256)
        set_rgb((0, 0, 0))
        time.sleep(0.01)
        set_rgb((r, g, b))
        time.sleep(0.01)

def police():
    while mode == 'police':
        set_rgb((255, 0, 0))
        time.sleep(0.25)
        set_rgb((0, 0, 255))
        time.sleep(0.25)

def random_colours():
    while mode == 'random':
        r = random.randrange(256)
        g = random.randrange(256)
        b = random.randrange(256)
        set_rgb((r, g, b))
        time.sleep(0.1)
        

def fade_all():
    h = 0
    s = 1
    v = 255

    huestep = 0.005

    run = True
    while mode == 'fade':
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        set_rgb((r, g, b))
        time.sleep(0.1)
        h = h + huestep
        if h >= 1:
            h = 0

def cycle_colours():
    while True:
        set_rgb((255, 0, 0))
        time.sleep(0.5)
        set_rgb((255, 255, 0))
        time.sleep(0.5)
        set_rgb((0, 255, 0))
        time.sleep(0.5)
        set_rgb((0, 255, 255))
        time.sleep(0.5)
        set_rgb((0, 0, 255))
        time.sleep(0.5)
        set_rgb((255, 0, 255))
        time.sleep(0.5)

def main():
    print 'Main loop starting'
    currentmode = ''
    while True:
        currentmode = main_loop(currentmode)

def main_loop(currentmode):
    if currentmode != mode:
        print 'Changing mode: %s' % mode
        if mode == 'fade':
            fade_all()
        elif mode == 'random':
            random_colours()
        elif mode == 'randstrobe':
            randstrobe()
        elif mode == 'strobe':
            strobe()
        elif mode == 'police':
            police()
        else:
            set_colour(mode)
        currentmode = mode
    time.sleep(1)
    return currentmode


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        global mode
        if 'text' in data:
            tweet = data['text'].encode('utf-8')
            print 'Received tweet: %s' % tweet
            #set_colour(tweet)
            mode = parse_colour(tweet)

    def on_error(self, status_code, data):
        print 'Twitter error %s' % status_code

        # stop trying to get data because of the error?
        # self.disconnect()

def start_twitter():
    print "Twitter thread started"
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    stream = MyStreamer(APP_KEY, APP_SECRET, ACCESS_KEY, ACCESS_SECRET)
    stream.statuses.filter(track=WATCH)

def start_twitter_thread():
    print "Starting twitter thread"
    t = threading.Thread(target=start_twitter)
    t.daemon = True
    t.start()

#set_colour(sys.argv[1])
#fade_colour((255, 0, 0), (0, 0, 255))
#cycle_colours()
if len(sys.argv) > 1:
    mode = sys.argv[1]
    main_loop('')
else:
    start_twitter_thread()
    main()

