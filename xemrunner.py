import os
import sys
import json
import requests
import time
import tweepy
from time import gmtime, strftime
from exceptions import BaseException
from traceback import format_exc
import sqlite3
import commands
import logging

''' Check, Store each Liquidation '''
def gotXem():
   return True

def getXem():

   pair = "BTC_XEM"
   url = "https://poloniex.com/public?command=returnTicker"
   msgs = []

   try:
     r = requests.get(url)
     price = r.json()[pair]["last"]
     msg = "Latest price for %s @ Poloniex : %s " % (pair,price)
     msgs.append(msg)
   except BaseException as ex:
     print(format_exc())
     return ""   

   return msgs

''' Write Xem details to Twitter using details from getRekage '''
def WriteXem(msgs):

   if msgs is None or len(msgs) == 0: 
     return

   # Consumer keys and access tokens
   app_key             = 'S2X7ea1hyUpS2ODi31YkPZFYw'
   app_secret          = 'ZbjW92l4ZcdWPpP30dmE4BlMDYfgL23idwX33hVE2QOivvJhOR'
   access_token        = '883905178486710272-wmeoOHKrk26NyKvrKGzc3egPvtXemh2'
   access_token_secret = 'p1tDRNoLqJct9234EifvQNoUoSiltducyzfsUE3Gihiye'

   auth = tweepy.OAuthHandler(app_key,app_secret)
   auth.set_access_token(access_token,access_token_secret)
   api = tweepy.API(auth)
   for msg in msgs:
      try:
         print("Sending twitter update '%s' " % msg)
         api.update_status(msg)
      except BaseException as ex:
         print(format_exc())

if __name__ == "__main__":

   SLEEPTIME = 300 # seconds

   run = None    
   while run != 'n':
      Xem = getXem()
      if Xem:
         WriteXem(Xem)
      print('Sleeping ...')
      time.sleep(SLEEPTIME) 
   print('Closing XEM ...')
