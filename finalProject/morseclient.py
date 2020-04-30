# Toby Sterk
# CS 300
# 22 April 2020
# Final Project

# USE WIRINGPI TO GET ACCURATE TIMING

# Imports
import time as time
import RPi.GPIO as GPIO
from morsetranslater import MORSE_CODE_DICT, decrypt

# GPIO Constants
button = 12
led = 16

# Timing Constants (based off https://morsecode.world/international/timing.html)
s_ms_conversion = 1000
bounce_time = 200 # in ms
time_unit = 300 # in ms
short_char_length = 1 * time_unit # in ms
short_char = '.'
long_char_length = 3 * time_unit # in ms
long_char = '-'
letter_gap_length = 3 * time_unit # in ms
word_gap_length = 7 * time_unit # in ms

# State Constants
WAIT = "wait_state"
FIN_WORD = "finish_word_state"
FIN_LETTER = "finish_letter_state"


# Variables
startTime = 0
endTime = 0
currentCharStr = ""
message = ""
currentState = ""
buttonWasPressed = False # I could just compare startTime and endTime, but this is easier to read

# Set up GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP) # button
GPIO.setup(led, GPIO.OUT, initial = GPIO.LOW) # LED

def append_char(end_word = False):
    global currentCharStr, message
    message += decrypt(currentCharStr)
    currentCharStr = ""
    if end_word:
        message += " "

def button_callback(channel):
    global startTime, endTime
    if (startTime > endTime): # button pushed
        startTime = time.time()
        
        timeBetweenPresses = (startTime - endTime) * s_ms_conversion

        # check to see if new word or letter
        if (timeBetweenPresses > word_gap_length):
            append_char(end_word=True)
        elif (timeBetweenPresses > letter_gap_length):
            append_char(end_word=False)


    else: # button released, determine new char

        endTime = time.time()
        timePressed = (endTime - startTime) * s_ms_conversion
        print("Time change is " + str(timePressed) + " ms")

        # detect kind of press
        if (timePressed > long_char_length): # long press
            print(long_char)
            currentCharStr += long_char
        else: # short press
            print(short_char)
            currentCharStr += short_char

GPIO.add_event_detect(button, GPIO.BOTH, callback=button_callback, bouncetime=bounce_time)

# Main loop
while(True):
    print("Hi")

print("Sleep for 15 seconds to wait for input")
time.sleep(15)
print("All done!")

GPIO.cleanup()
