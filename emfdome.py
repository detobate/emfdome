from twython import Twython
from twython import TwythonStreamer
from decimal import *
import time
import os
import webcolors
import re
 
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

def pwm(pin, angle):
    cmd = "echo " + str(pin) + "=" + str(angle) + " > /dev/pi-blaster"
    os.system(cmd)
    time.sleep(DELAY)

def test_tweet(thing):
    try: 
        float(thing)
        return thing
    except ValueError: 
        pass

def set_colour(tweet):
    r = None
    g = None
    b = None
    tweet.lower()
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
    
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
        r = str(Decimal(r) / 255)
        g = str(Decimal(g) / 255)
        b = str(Decimal(b) / 255)
        print 'Red: ', r, ' Green: ', g, ' Blue: ', b
        pwm(R, r)
        pwm(G, g)
        pwm(B, b)
        #twitter.update_status(status='Dome set to Red:"%s" Green:"%s" Blue:"%s"' % (r,g,b)) 
    else:
        print 'Invalid RGB value. RGB needs to be between 0 and 255'


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            tweet = data['text'].encode('utf-8')
            set_colour(tweet)

    def on_error(self, status_code, data):
        print status_code
        # stop trying to get data because of the error?
        # self.disconnect()

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
stream = MyStreamer(APP_KEY, APP_SECRET, ACCESS_KEY, ACCESS_SECRET)
stream.statuses.filter(track=WATCH)
