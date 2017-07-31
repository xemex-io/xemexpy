import os
import sys
import json
import requests
import time
import tweepy
from traceback import format_exc
from flask import Flask

app = Flask(__name__)

@app.route('/')
def about():
    return 'XemexPY: v0.0.1'

@app.route('/price')
def price():
   msg = None
   pair = "BTC_XEM"
   url = "https://poloniex.com/public?command=returnTicker"
   try:
     r = requests.get(url)
     price = r.json()[pair]["last"]
     msg = "Latest price for %s @ Poloniex : %s" % (pair,price)
   except BaseException as ex:
     print(format_exc())
     return ""
   if msg:
      WriteXem(msg)
   return msg

''' Write Xem details to Twitter using details from getRekage '''
def WriteXem(msg):

    if msg is None or len(msg) == 0: 
        return

    # Consumer keys and access tokens
    app_key             = 'S2X7ea1hyUpS2ODi31YkPZFYw'
    app_secret          = 'ZbjW92l4ZcdWPpP30dmE4BlMDYfgL23idwX33hVE2QOivvJhOR'
    access_token        = '883905178486710272-wmeoOHKrk26NyKvrKGzc3egPvtXemh2'
    access_token_secret = 'p1tDRNoLqJct9234EifvQNoUoSiltducyzfsUE3Gihiye'

    auth = tweepy.OAuthHandler(app_key,app_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth)
    try:
        print("Sending twitter update '%s' " % msg)
        api.update_status(msg)
    except BaseException as ex:
        print(format_exc())

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
