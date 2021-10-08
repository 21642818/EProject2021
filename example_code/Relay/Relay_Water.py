import RPi.GPIO as GPIO
import time

Relay_Ch_1 = 5
Relay_Ch_2 = 6
Relay_Ch_3 = 13
Relay_Ch_4 = 19
Relay_Ch_5 = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(Relay_Ch_1, GPIO.OUT)
GPIO.setup(Relay_Ch_2, GPIO.OUT)
GPIO.setup(Relay_Ch_3, GPIO.OUT)
GPIO.setup(Relay_Ch_4, GPIO.OUT)
GPIO.setup(Relay_Ch_5, GPIO.OUT)
GPIO.output(Relay_Ch_1, GPIO.LOW)
GPIO.output(Relay_Ch_2, GPIO.LOW)
GPIO.output(Relay_Ch_3, GPIO.LOW)
GPIO.output(Relay_Ch_4, GPIO.LOW)
GPIO.output(Relay_Ch_5, GPIO.LOW)
time.sleep(2)

print("START")
try:
    while 1:
        GPIO.output(Relay_Ch_1, GPIO.HIGH)
	GPIO.output(Relay_Ch_5, GPIO.HIGH)
        print("Dripper 1 is on")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_1, GPIO.LOW)
	GPIO.output(Relay_Ch_5, GPIO.LOW)
        print("Dripper 1 is off")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_2, GPIO.HIGH)
        GPIO.output(Relay_Ch_5, GPIO.HIGH)
        print("Dripper 2 is on")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_2, GPIO.LOW)
        GPIO.output(Relay_Ch_5, GPIO.LOW)
        print("Dripper 2 is off")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_3, GPIO.HIGH)
        GPIO.output(Relay_Ch_5, GPIO.HIGH)
        print("Dripper 3 is on")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_3, GPIO.LOW)
        GPIO.output(Relay_Ch_5, GPIO.LOW)
        print("Dripper 3 is off")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_4, GPIO.HIGH)
        GPIO.output(Relay_Ch_5, GPIO.HIGH)
        print("Dripper 4 is on")
        time.sleep(1.5)
        GPIO.output(Relay_Ch_4, GPIO.LOW)
        GPIO.output(Relay_Ch_5, GPIO.LOW)
        print("Dripper 4 is off")
        time.sleep(1.5)
except KeyboardInterrupt:
    GPIO.cleanup()

