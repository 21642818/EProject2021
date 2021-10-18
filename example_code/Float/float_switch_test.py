import RPi.GPIO as GPIO
import time

float_sw = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(float_sw, GPIO.IN)

while True:
    state = GPIO.input(float_sw)
    print('Float Switch:', state)
    time.sleep(0.5)