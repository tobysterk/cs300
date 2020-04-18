# CS300 Lab 9 MQTT client
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import os

# Constants
BROKER = 'mqtt.eclipse.org'
PORT = 1883
QOS = 0
LED = 16
PIR = 18
DELAY = 1.0

# Initialize GPIO input and output
GPIO.setmode(GPIO.BCM) # Use BCM numbers
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(PIR, GPIO.IN)

# Callback when a message is published
def on_publish(client, userdata, mid):
    print("MQTT data published")

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print('Connected to',BROKER)
    else:
        print('Connection to',BROKER,'failed. Return code=',rc)
        os._exit(1)

# Callback when client receives a PUBLISH message from the broker
def on_message(client, data, msg):
    if msg.topic == "ths6/LED":
        print("Received message: LED = ", int(msg.payload))
        if int(msg.payload) == 1:
            GPIO.output(LED, True)
        elif int(msg.payload) == 0:
            GPIO.output(LED, False)

# Setup MQTT client and callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("ths6/LED", qos=QOS)
client.loop_start()

# Continuously publish changes in motion state
motion_state = 0
try:
    while True:
    # If motion state has changed, publish a message
        # Check for change in motion state
        if GPIO.input(PIR) != motion_state:
            motion_state = GPIO.input(PIR)
            print("motion =", motion_state)
            client.publish('ths6/motion', str(motion_state))
        time.sleep(DELAY)

except KeyboardInterrupt:
    print("\nDone")
    GPIO.cleanup()
    client.disconnect()