import RPi.GPIO as GPIO
import time

float_sw = 4
GPIO.setmode(GPIO.BCM)

GPIO.setup(float_sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    state = GPIO.input(float_sw)
    print('Float Switch:', state)
    time.sleep(0.5)