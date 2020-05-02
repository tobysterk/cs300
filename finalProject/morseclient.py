# Toby Sterk
# CS 300
# 22 April 2020
# Final Project

# USE WIRINGPI TO GET ACCURATE TIMING

# Imports
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from MorseTranslater import MorseTranslater
import os

# GPIO Constants
data_button = 16
led = 12
reset_button = 1

# Timing Constants (based off https://morsecode.world/international/timing.html)
s_ms_conversion = 1000
bounce_time = 200 # in ms
time_unit = 400 # in ms
short_char_length = 1 * time_unit # in ms
short_char = '.'
long_char_length = 3 * time_unit # in ms
long_char = '-'
letter_gap_length = 3 * time_unit # in ms
word_gap_length = 7 * time_unit # in ms

# MQTT Constants
BROKER = 'iot.cs.calvin.edu'
USERNAME = "cs300" # Put broker username here
PASSWORD = "safeIoT" # Put broker password here
PORT = 8883
QOS = 0
DELAY = 5.0
TOPIC = 'ths6/morse'
CERTS = '/etc/ssl/certs/ca-certificates.crt'

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
buttonIsPressed = False # I could just compare startTime and endTime, but this is easier to read
translater = MorseTranslater()
spaceEligible = False

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, flags, rc):
 if rc==0:
    print('Connected to',BROKER)
 else:
    print('Connection to',BROKER,'failed. Return code=',rc)
    os._exit(1)


# Translate and add the entered pattern
def append_char():
    global currentCharStr, message, spaceEligible, client
    try:
        message += translater.translate(currentCharStr)
        print(currentCharStr + " -> " + message)
        currentCharStr = ""
        spaceEligible = True
        client.publish(TOPIC, message)
    except KeyError: # key not found in dictionary because the entered pattern is wrong
        print("ERROR: Invalid character entered")
        currentCharStr = ""

# Add a space to the message
def append_space():
    global message, spaceEligible, client
    message += " "
    print("word ended")
    spaceEligible = False
    client.publish(TOPIC, message)

# Toggle buttonIsPressed boolean
def toggle_buttonIsPressed():
    global buttonIsPressed
    if (buttonIsPressed): # last button action was a press
        buttonIsPressed = False # this action is a release
    else : # last button action was a release
        buttonIsPressed = True # this action is a press

# Callback when the data button has an edge (rising or falling)
def data_button_callback(channel):
    global startTime, endTime, currentCharStr, buttonIsPressed
    toggle_buttonIsPressed() # if false, button press caused callback

    if (buttonIsPressed):
        startTime = time.time()  

    else: # button released, determine new char
        endTime = time.time()
        timePressed = (endTime - startTime) * s_ms_conversion
        # print("Time change is " + str(timePressed) + " ms")

        # detect kind of press
        if (timePressed > long_char_length): # long press
            print(long_char)
            currentCharStr += long_char
        else: # short press
            print(short_char)
            currentCharStr += short_char

def reset_button_callback(channel):
    global startTime, endTime, currentCharStr, message, buttonIsPressed

    startTime = 0
    endTime = 0
    currentCharStr = ""
    message = ""
    buttonIsPressed = False
    print("reset")


# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(data_button, GPIO.IN, pull_up_down = GPIO.PUD_UP) # data button
GPIO.setup(reset_button, GPIO.IN, pull_up_down = GPIO.PUD_UP) # reset button
GPIO.setup(led, GPIO.OUT, initial = GPIO.LOW) # LED

GPIO.add_event_detect(data_button, GPIO.BOTH, callback=data_button_callback, bouncetime=bounce_time)
GPIO.add_event_detect(reset_button, GPIO.RISING, callback=reset_button_callback, bouncetime = bounce_time)

# Setup MQTT client and callbacks
client = mqtt.Client()
client.on_connect = on_connect
# Securely connect to MQTT broker
client.username_pw_set(USERNAME, password=PASSWORD)
client.tls_set(CERTS)
client.connect(BROKER, PORT, 60)
client.loop_start()

# Main loop
try:
    while(True):
        GPIO.output(led, True)
        time.sleep(time_unit / (s_ms_conversion)) # on for a time unit
        GPIO.output(led, False)
        time.sleep(time_unit / (s_ms_conversion)) # off for a time unit

        timeBetweenPresses = (time.time() - endTime) * s_ms_conversion

        if (not buttonIsPressed) and (currentCharStr):
            # if button is not pressed and a pattern has been entered since the last translation
            
            if timeBetweenPresses > letter_gap_length: # check to see if new letter
                append_char()
                
        elif (not buttonIsPressed) and (not currentCharStr) and (endTime != 0):
            if timeBetweenPresses > (word_gap_length - letter_gap_length) and spaceEligible:
                append_space()

except KeyboardInterrupt: # Allow for nice shutdown when someone presses ^C
    print("\nExiting...")
finally:
    GPIO.cleanup()
