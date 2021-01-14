import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)  # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 17  # pin 11
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)  # GPIO Assign mode


def click() -> None:
    '''Makes one click and releases the relay'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
    time.sleep(1)
    GPIO.cleanup()


def test_click():
    print('CLICK!')
