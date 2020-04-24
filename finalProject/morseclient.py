# Toby Sterk
# CS 300
# 22 April 2020
# Final Project

# USE WIRINGPI TO GET ACCURATE TIMING

# Imports
import time as time
import RPi.GPIO as GPIO
from morsetranslater import MORSE_CODE_DICT, decrypt

# Constants
button = 12
led = 16
timeUnit = 200 # in milliseconds
ms_ns_conversion = 1000000

# Variables
startTime = 0
endTime = 0

# Set up GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP) # button
GPIO.setup(led, GPIO.OUT, initial = GPIO.LOW) # LED

def record_callback(channel):
    global startTime, endTime
    if (startTime == 0): # button pushed, start recording
        startTime = time.time_ns()
        print(startTime)
    else: # button released, finish/process recording
        endTime = time.time_ns()
        print(endTime)
        if ((endTime - endTime) // ms_ns_conversion > timeUnit):
            # record dash
            print('-')
        else:
            # record dot
            print('.')
        # reset startTime and endTime
        startTime = 0
        endTime = 0


GPIO.add_event_detect(button, GPIO.BOTH, callback=record_callback, bouncetime=200)


print("Sleep for 15 seconds to wait for input")
time.sleep(15)
print("All done!")

GPIO.cleanup()
