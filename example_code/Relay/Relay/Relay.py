import RPi.GPIO as GPIO
import time

Relay_Ch_1 = 20
Relay_Ch_2 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(Relay_Ch_1, GPIO.OUT)
GPIO.output(Relay_Ch_1, GPIO.LOW)
time.sleep(10)

print("START")
try:
    while 1:
        GPIO.output(Relay_Ch_1, GPIO.HIGH)
        print("Ch1 is on")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_1, GPIO.LOW)
        print("Ch1 is off")
        time.sleep(1.5)
except KeyboardInterrupt:
    GPIO.cleanup()

