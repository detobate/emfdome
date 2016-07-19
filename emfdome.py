#!/usr/bin/python
from twython import TwythonStreamer
import re, webcolors, Queue, threading
from twitterkeys import *
from emfdome import *

STEP = 100
DELAY = 0.5

# OAUTH2 Keys, imported from twitterkeys
"""
APP_KEY = ''
APP_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
"""

# servo to pin mapping
pins = {'R': 18,
        'G': 23,
        'B': 24
         }

""" Alternative mappings
pins = {'R': 4,
        'G': 17,
        'B': 18
        } """

# Keyword
WATCH = '@emfdome'
mode = 'fade'

# Was using tuples for predefined colours, but managing another type was becoming a pain
presets = {'blue': '0 0 255',
            'red': '255 0 0',
            'green': '0 255 0',
            'fade': 'fade',
            'strobe': 'strobe',
            'randstrobe': 'randstrobe',
            'police': 'police',
            'cycle': 'cycle'
           }

def test_tweet(thing):
    try: 
        float(thing)
        return thing
    except ValueError: 
        pass

def parse_colour(tweet):

    # Look for a valid keyword anywhere in the tweet
    parts = tweet.lower().split(" ")
    for i in range(len(parts)):
        if parts[i] in presets:
            return presets[parts[i]]
        elif parts[i][0] == '#':
            try:
                value = webcolors.hex_to_rgb(parts[i])
                mode = "%s %s %s" % (str(value[0]), str(value[1]), str(value[2]))
                return mode
            except:
                print('%s is not a webcolor' % str(parts[i]))
                pass

    # Look for a trio of digits
    m = re.search('(\d+ \d+ \d+)', tweet.lower())
    if m:
        return m.group(0)

    print('Couldn\'t parse %s' % tweet)
    return None


def set_colour(leds, tweet):
    r = None
    g = None
    b = None

    foo = tweet.split(" ")
    for i in range(len(foo)):
        value = test_tweet(foo[i])
        if value is not None:
            if r is None:
                r = int(value)
            elif g is None:
                g = int(value)
            elif b is None:
                b = int(value)
    print('set_color calling set_rgb with (%s, %s, %s)' % (r, g, b))
    leds.set_rgb((r, g, b))

def start_preset(leds, mode):
    preset = Presets(leds)
    preset.change(mode)

def start_twitter():
    stream = MyStreamer(APP_KEY, APP_SECRET, ACCESS_KEY, ACCESS_SECRET)
    stream.statuses.filter(track=WATCH)

def start_twitter_thread():
    t = threading.Thread(target=start_twitter)
    t.daemon = True
    t.start()
    print "Twitter listener thread started"

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        if 'text' in data:
            tweet = data['text'].encode('utf-8')
            print('Received tweet: %s' % str(tweet))
            response = parse_colour(tweet)
            if response is not None:
                print('on_success adding %s to the queue' % str(response))
                queue.put(response)

    def on_error(self, status_code, data):
        print('Twitter error %s' % status_code)

def main():

    # Create a globally available queue that our twitter thread can add to
    global queue
    queue = Queue.Queue(42)
    # Create a LightStrip object with the defined pins
    leds = LightStrip(pins)
    print('Starting Twitter Listener')
    start_twitter_thread()

    while True:
        if queue.empty():
            time.sleep(1)
            pass
        else:
            newTweet = queue.get()
            if newTweet is not None:
                change_mode(newTweet, leds)
            queue.task_done()


def change_mode(mode, leds):
    print('Changing mode to: %s' % str(mode))
    # This is a bit lame, could do with a tidy up at some point
    if mode in presets:
        print('Starting preset thread with mode %s' % mode)
        p = threading.Thread(target=start_preset, args=(leds,mode))
        p.daemon = True
        p.start()

    else:
        set_colour(leds, mode)

    # Keep track of the current mode
    leds.mode = mode  # This assumes we get a match. Should probably fix

if __name__ == "__main__":
    main()