# CS300 MQTT Lab
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Constants
BROKER = 'mqtt.eclipse.org' # Set the MQTT broker (change if needed)
PORT = 1883
QOS = 0
IN = 12
MESSAGE = 'Button pressed'

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Use GPIO 12 as button inputs
GPIO.setup(IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup MQTT client and callbacks
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Callback function when button is pressed
def button_callback(channel):
 global client
 (result, num) = client.publish('ths6/button', MESSAGE, qos=QOS)
 if result != 0:
 print('PUBLISH returned error:', result)

# Detect a falling edge on input pin
GPIO.add_event_detect(IN, GPIO.FALLING, callback=button_callback, bouncetime=500)

client.loop_start()
while True:
 time.sleep(10)
 
print("Done")
client.disconnect()
GPIO.cleanup() # clean up GPIO