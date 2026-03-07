import os
import requests
import tweepy
from traceback import format_exc
from flask import Flask

app = Flask(__name__)


def get_twitter_credentials():
    return {
        "app_key": os.environ.get("TWITTER_API_KEY") or os.environ.get("TWITTER_APP_KEY"),
        "app_secret": os.environ.get("TWITTER_API_SECRET") or os.environ.get("TWITTER_APP_SECRET"),
        "access_token": os.environ.get("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
    }

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
   except BaseException:
     print(format_exc())
     return ""
   if msg:
      WriteXem(msg)
   return msg

''' Write Xem details to Twitter using details from getRekage '''
def WriteXem(msg):

    if msg is None or len(msg) == 0: 
        return

    credentials = get_twitter_credentials()
    if not all(credentials.values()):
        print("Twitter credentials not configured; skipping status update.")
        return

    auth = tweepy.OAuthHandler(credentials["app_key"], credentials["app_secret"])
    auth.set_access_token(credentials["access_token"], credentials["access_token_secret"])
    api = tweepy.API(auth)
    try:
        print("Sending twitter update '%s' " % msg)
        api.update_status(msg)
    except BaseException:
        print(format_exc())

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
