#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import datetime
from datetime import timedelta
import requests

SigPin = 11    # pin11

lastclick = datetime.datetime.now()
 
def button(ev=None):
   global lastclick
   now = datetime.datetime.now()
   if(now-lastclick > timedelta(seconds=2)):
      lastclick = datetime.datetime.now()
      print 'shoot'
      r= requests.put('http://127.0.0.1/pictures/take')
      print r.status_code
      print r.json()

def setup():
   GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
   GPIO.setup(SigPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set Pin's mode is input, and pull up to high level(3.3V)
   GPIO.add_event_detect(SigPin, GPIO.RISING, callback=button) # wait for rasing

def loop():
   while True:
      time.sleep(1)
def destroy():
   GPIO.cleanup()    # Release resource

if __name__ == '__main__':     # Program start from here
   setup()
   try:
      loop()
   except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
      destroy()
destroy()
