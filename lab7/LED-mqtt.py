# CS300 MQTT Lab
import RPi.GPIO as GPIO
import time as time
import paho.mqtt.client as mqtt

# Constants
BROKER = 'mqtt.eclipse.org'
PORT = 1883
QOS = 0
LEDY = 16
LEDR = 15
TOPIC_YELLOW = 'dma2/LEDY'
TOPIC_RED = 'dma2/LEDR'


# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Configure GPIO for LED output
GPIO.setup(LEDY, GPIO.OUT)
GPIO.setup(LEDR, GPIO.OUT)

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, rc, *extra_params):
    print('Connected with result code='+str(rc))

# Callback when client receives a message from the broker
# Use button message to turn LED on/off
def on_message(client, data, msg):
    print(msg.topic)
    if msg.topic == TOPIC_YELLOW:
        if GPIO.input(LEDY) == 1:
            GPIO.output(LEDY, 0)
        else:
            GPIO.output(LEDY, 1)
		
    else:
        if GPIO.input(LEDR) == 0:
            GPIO.ouput(LEDR, 1)
        else:
            GPIO.output(LEDR, 0)

#Main program
try:
  # Setup MQTT client and callbacks
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  # Connect to MQTT broker and subscribe to the button topic
  client.connect(BROKER, PORT, 60)
  client.subscribe(TOPIC_YELLOW, qos=QOS)
  client.subscribe(TOPIC_RED, qos=QOS)
  client.loop_start()

  client.loop_start()
  while True:
      time.sleep(10)
except KeyboardInterrupt:
  print("Done.. program closed")
finally:
  client.disconnect()
  GPIO.cleanup() # clean up GPIO
