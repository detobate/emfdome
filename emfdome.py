#!/usr/bin/python

import re, threading, webcolors, Queue
from twython import TwythonStreamer
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
#R = '4'
#G = '17'
#B = '18'
pins = {'R': 18,
        'G': 23,
        'B': 24
         }

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

    # Look for a trio of digits
    m = re.search('(\d+ \d+ \d+)', tweet.lower())
    if m:
        return m.group(0)
    else:
        print('Couldn\'t parse %s' % tweet)

    print("parse_colour returning None")
    return None


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
                print foo[i] + ' is not a valid webcolor'
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
    print('set_color calling set_rgb with (%s, %s, %s)' % (r, g, b))
    set_rgb(pins, (r, g, b))
    


def main():

    # Create a globally available queue that our twitter thread can add to
    global queue
    queue = Queue.Queue(42)
    print('Starting Twitter Listener')
    start_twitter_thread()

    while True:
        if queue.empty():
            time.sleep(1)
            pass
        else:
            newTweet = queue.get()
            if newTweet is not None:
                # Keep track of the current mode although we don't do anything with it yet
                current_mode = main_loop(newTweet)
            queue.task_done()


def main_loop(mode):
    print('Changing mode: %s' % str(mode))
    if mode == 'fade':
        fade_all(pins, queue)    # We still need to pass queue to functions from modules, because py namespaces.
    elif mode == 'random':
        random_colours(pins, queue)
    elif mode == 'randstrobe':
        randstrobe(pins, queue)
    elif mode == 'strobe':
        strobe(pins, queue)
    elif mode == 'police':
        police(pins, queue)
    else:
        set_colour(mode)
    currentmode = mode  # This assumes we get a match. Should probably fix
    return currentmode


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

def start_twitter():
    stream = MyStreamer(APP_KEY, APP_SECRET, ACCESS_KEY, ACCESS_SECRET)
    stream.statuses.filter(track=WATCH)

def start_twitter_thread():
    t = threading.Thread(target=start_twitter)
    t.daemon = True
    t.start()
    print "Twitter listener thread started"

if __name__ == "__main__":
    main()

