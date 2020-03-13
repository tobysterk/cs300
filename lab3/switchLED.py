import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP) # button
GPIO.setup(16, GPIO.OUT, initial = GPIO.LOW) # LED

def toggleLED_callback(channel):
    if GPIO.input(16) == 0:     # LED is off
        GPIO.output(16, True)
    else:                       # LED is on
        GPIO.output(16, False)

GPIO.add_event_detect(12, GPIO.FALLING, callback=toggleLED_callback, bouncetime=200)

print("Sleep for 15 seconds to wait for input")
time.sleep(15)
print("All done!")

GPIO.cleanup()