import time
import os
import numpy as np
import RPi.GPIO as GPIO
from datetime import datetime
from ADC import ADCPi
from sht20 import SHT20
from picamera import PiCamera

class SmartPlant:

    __Relay_Ch_1 = 5
    __Relay_Ch_2 = 6
    __Relay_Ch_3 = 13
    __Relay_Ch_4 = 19
    __Relay_Ch_5 = 26

    def __init__(self) -> None:
        
        #initialize ADC
        self.__adc = ADCPi(0x68, 18)
        self.__adc.set_pga(2)

        #initialize Camera
        self.__camera = PiCamera(resolution = (3280, 2464), sensor_mode=3)

        #initialize Temp&Hum sensor
        self.__sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)

    def gpio_init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__Relay_Ch_1, GPIO.OUT)
        GPIO.setup(self.__Relay_Ch_2, GPIO.OUT)
        GPIO.setup(self.__Relay_Ch_3, GPIO.OUT)
        GPIO.setup(self.__Relay_Ch_4, GPIO.OUT)
        GPIO.setup(self.__Relay_Ch_5, GPIO.OUT)
        GPIO.output(self.__Relay_Ch_1, GPIO.LOW)
        GPIO.output(self.__Relay_Ch_2, GPIO.LOW)
        GPIO.output(self.__Relay_Ch_3, GPIO.LOW)
        GPIO.output(self.__Relay_Ch_4, GPIO.LOW)
        GPIO.output(self.__Relay_Ch_5, GPIO.LOW)

    def get_relay(self, channel):
        if channel == 0:
            return self.__Relay_Ch_1
        elif channel == 1:
            return self.__Relay_Ch_2
        elif channel == 2:
            return self.__Relay_Ch_3
        elif channel == 3:
            return self.__Relay_Ch_4
        elif channel == 4:
            return self.__Relay_Ch_5
        else: 
            raise Exception("get_relay: Value {} is not valid".format(channel))
    
    def set_relay(self, relay_channels):
        # TODO: Relpace time.sleep with something else. This halts the program and we don't want it
        self.gpio_init()
        for r in range(5):
            GPIO.output(self.get_relay(r), relay_channels[r])
        time.sleep(2)
        for r in range(5):
            GPIO.output(self.get_relay(r), GPIO.LOW)
        GPIO.cleanup()
        # NOTE  Use GPIO.cleanup() after exit

    def get_moisture(self, channel):
        # NOTE Max voltage of Soil Sensor out of soil is 5.060569V, submersed is 3.0831282V
        voltage = self.__adc.read_voltage(channel)
        level = ( (5.060569 - voltage)/(5.060569 - 3.0831282) ) * 100
        return level
    
    def read_moisture_levels(self):
        return [self.get_moisture(1), self.get_moisture(2), self.get_moisture(3), self.get_moisture(4) ]

    def capture_image(self):
        self.__camera.start_preview()
        time.sleep(5)
        #now = datetime.now()
        #d = now.strftime("%m%d%Y_%H%M%S")
        self.__camera.capture('%s.jpg',datetime.now().strftime("%m%d%Y_%H%M%S"))
        self.__camera.stop_preview()