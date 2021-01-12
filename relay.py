import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers


print("Start")
RELAIS_1_GPIO = 17 #pin 11
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode

for i in range(3):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
	GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
	time.sleep(1)
	GPIO.cleanup()
	time.sleep(1)

# GPIO.output(RELAIS_1_GPIO, 1) # out
# time.sleep(2)
# print("GPIO LOW")
# GPIO.output(RELAIS_1_GPIO, 0) # out
# time.sleep(2)
# GPIO.cleanup()

# print("GPIO HIGH")
# GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
# time.sleep(5)
print("Exit")
