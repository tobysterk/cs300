# Toby Sterk and Daniel Ackuaku
# CS 300
# 13 February 2020
# HW 1

# Imports
import time as time
import RPi.GPIO as GPIO

# Constants
STATE1 = "STATE_1"
STATE2 = "STATE_2"
STATE3 = "STATE_3"
STATE4 = "STATE_4"
STATE5 = "STATE_5"
STATE6 = "STATE_6"

LED1 = 23
LED2 = 24
LED3 = 25
LED4 = 16
LED5 = 20
LED6 = 21
SWITCH = 14

# Variables 
direction = "FWD"
currentState = STATE1

# Function declarations 
def switchPressed(channel):
    global direction 
    if direction == "FWD" and currentState != STATE6:
        direction = "REV"
    elif currentState != STATE1 and currentState != STATE5: 
        direction = "FWD"

# Initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1, GPIO.OUT, initial = GPIO.LOW) #23
GPIO.setup(LED2, GPIO.OUT, initial = GPIO.LOW) #24
GPIO.setup(LED3, GPIO.OUT, initial = GPIO.LOW) #25
GPIO.setup(LED4, GPIO.OUT, initial = GPIO.LOW) #16
GPIO.setup(LED5, GPIO.OUT, initial = GPIO.LOW) #20
GPIO.setup(LED6, GPIO.OUT, initial = GPIO.LOW) #21
GPIO.setup(SWITCH, GPIO.IN, pull_up_down = GPIO.PUD_UP) #14
GPIO.add_event_detect(SWITCH, GPIO.RISING, callback=switchPressed,bouncetime=250) #switch callback


# State Machine

# In a given state:
#   Turn the corresponding LED on
#   Sleep
#   (If STATE1 or STATE6) Change direction
#   Update state
#   Turn off the corresponding LED
try:
    while (1):
        if currentState == STATE1:
            GPIO.output(LED1, True)
            time.sleep(0.2)
            direction = "FWD"
            currentState = STATE2
            GPIO.output(LED1, False)

        elif currentState == STATE2:
            GPIO.output(LED2, True)
            time.sleep(0.2)
            if direction == "FWD":
                currentState = STATE3
            else: 
                currentState = STATE1
            GPIO.output(LED2, False)
        
        elif currentState == STATE3:
            GPIO.output(LED3, True)
            time.sleep(0.2)
            if direction == "FWD":
                currentState = STATE4
            else: 
                currentState = STATE2
            GPIO.output(LED3, False)

        elif currentState == STATE4:
            GPIO.output(LED4, True)
            time.sleep(0.2)
            if direction == "FWD":
                currentState = STATE5
            else: 
                currentState = STATE3
            GPIO.output(LED4, False)

        elif currentState == STATE5:
            GPIO.output(LED5, True) 
            time.sleep(0.2)
            if direction == "FWD":
                currentState = STATE6
            else: 
                currentState = STATE4
            GPIO.output(LED5, False)    

        elif currentState == STATE6:
            GPIO.output(LED6, True)
            time.sleep(0.2)
            direction = "REV"
            currentState = STATE5
            GPIO.output(LED6, False)
except KeyboardInterrupt: # Allow for nice shutdown when someone presses ^C
    print("Bye Bye ...")
finally:
    GPIO.cleanup()