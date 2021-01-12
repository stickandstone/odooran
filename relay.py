import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers


print("Start")
RELAIS_1_GPIO = 17 #pin 11
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
print("GPIO LOW")
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
time.sleep(5)
print("GPIO HIGH")
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
time.sleep(5)
print("Exit")