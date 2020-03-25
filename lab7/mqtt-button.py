# CS300 MQTT Lab
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# Constants
BROKER = 'mqtt.eclipse.org' # Set the MQTT broker (change if needed)
PORT = 1883
QOS = 0
SW_YELLOW = 12
TOPIC_YELLOW = 'dma2/LEDY'
SW_RED = 16
TOPIC_RED = 'dma2/LEDR'
MESSAGE = 'Button pushed'

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Use GPIO 12 as button inputs
GPIO.setup(SW_YELLOW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_RED, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup MQTT client and callbacks
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Callback function when button is pressed
def button_callback(channel):
    global client
    
    # Determine topic based on channel
    topic = ""
    if channel == SW_YELLOW :
        topic = TOPIC_YELLOW
    elif channel == SW_RED:
        topic = TOPIC_RED

    # Publish message
    (result, num) = client.publish(topic, MESSAGE, qos=QOS)

    # Print feedback
    if result != 0:
        print('PUBLISH returned error:', result)
    else :
        if topic == TOPIC_YELLOW:
            print("Yellow button pressed")
        elif topic == TOPIC_RED:
            print("Red button pressed")

# Detect a falling edge on input pin
GPIO.add_event_detect(SW_YELLOW, GPIO.FALLING, callback=button_callback, bouncetime=500)
GPIO.add_event_detect(SW_RED, GPIO.FALLING, callback=button_callback, bouncetime=500)

# Main loop
try:
    client.loop_start()
    while True:
        time.sleep(10)

    print("Done")
    client.disconnect()
    GPIO.cleanup() # clean up GPIO

except KeyboardInterrupt:
    print("") # Prints a newline so the terminal looks good
finally:
    client.disconnect()
    GPIO.cleanup()
