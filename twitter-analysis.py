#!/usr/bin/env python
from __future__ import absolute_import, print_function

from tweepy import OAuthHandler, Stream, StreamListener
import json
import logging

from logging.handlers import TimedRotatingFileHandler

fin=open("keywords.txt", "r")
# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="xxx"
consumer_secret="xxx"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="xxx"
access_token_secret="xxx"

mylogger = logging.getLogger("Rotating Log")
mylogger.setLevel(logging.INFO)
myhandler = TimedRotatingFileHandler("logs/tweets")
mylogger.addHandler(myhandler)

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        global mylogger
        #print(data)
        twitter_data = json.loads(data)
        if 'text' in twitter_data:
            print(twitter_data['user']['screen_name'], "-", twitter_data['text'])
            mylogger.info(data.strip())
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    keywords = []
    for f in fin.readlines():
        keywords.append(f.strip())
    print(keywords)
#    exit()
    stream = Stream(auth, l)
    stream.filter(track=keywords)