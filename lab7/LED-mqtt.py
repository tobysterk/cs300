# CS300 MQTT Lab
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Constants
BROKER = 'mqtt.eclipse.org'
PORT = 1883
QOS = 0
LED = 16
MESSAGE = 'Button pressed'

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Configure GPIO for LED output
GPIO.setup(LED, GPIO.OUT)

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, rc, *extra_params):
 print('Connected with result code='+str(rc))

# Callback when client receives a message from the broker
# Use button message to turn LED on/off
def on_message(client, data, msg):
 if msg.topic == "ths6/button":
 if GPIO.input(LED) == 1:
 GPIO.output(LED, 0)
 else:
 GPIO.output(LED, 1)

# Setup MQTT client and callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("ths6/button", qos=QOS)
client.loop_start()
client.loop_start()
while True:
 time.sleep(10)

print("Done")
client.disconnect()
GPIO.cleanup() # clean up GPIO