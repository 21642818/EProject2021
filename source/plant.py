import time
import os
import json
import numpy as np
import RPi.GPIO as GPIO
from datetime import datetime
from ADC import ADCPi
from sht20 import SHT20
from picamera import PiCamera

class SmartPlant:

    __data = {}
    __last_img = None
    __Relay_Ch_1 = 5
    __Relay_Ch_2 = 6
    __Relay_Ch_3 = 13
    __Relay_Ch_4 = 19
    __Relay_Ch_5 = 26
    __Float_sw = 21

    def __init__(self) -> None:

        #initialize ADC
        self.__adc = ADCPi(0x68, 18)
        self.__adc.set_conversion_mode(0)

        #initialize Camera
        self.__camera = PiCamera()
        self.__camera.resolution = (3280, 2464)

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
        '''
        Returns the relay channel pin 

        :return: channel
        :rtype: int
        '''
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

    def set_relay(self, relay_channels, duration=2):
        '''
        Sets the relays to high or low for a duration

        :param relay_channel: 1 to 5
        :type relay_channel: int
        :param duration: seconds, defaults to 2
        :type duration: int
        '''
        # TODO Relpace time.sleep with something else. This halts the program and we don't want it
        if self.read_float_switch == 0:
            self.gpio_init()
            for r in range(5):
                GPIO.output(self.get_relay(r), relay_channels[r])
            time.sleep(duration)
            for r in range(5):
                GPIO.output(self.get_relay(r), GPIO.LOW)
            GPIO.cleanup()
        else:
            print("Error: water level is too low")
            # NOTE  Use GPIO.cleanup() after exit

    def get_moisture(self, channel):
        '''
        Returns the moisture level of the ADC channel

        :param channel: 1 to 4
        :type channel: int
        :return: level
        :rtype: float
        '''
        # NOTE Max voltage of Soil Sensor out of soil is 5.060569V, submersed is 2.929132167V
        voltage = self.__adc.read_voltage(channel)
        level = ( (5.060569 - voltage)   /(5.060569 - 2.929132167) ) * 100
        if (level < 0) and (level > 100):
            level = None
        return level

    def read_moisture_levels(self):
        '''
        Returns array of moisture levels from ADC channels 1 to 4
        in the format [ channel_1, channel_2, channel_3, channel_4]

        :return: moisture of channels
        :rtype: list
        '''
        return [self.get_moisture(1), self.get_moisture(2), self.get_moisture(3), self.get_moisture(4) ]

    def capture_image(self):
        '''
        Captures image with timestamp to './img/' and returns the filename

        :return: filename
        :rtype: string
        '''
        self.__camera.start_preview()
        # TODO Replace time.sleep() with something else
        time.sleep(5)
        date_time=datetime.now().strftime("%m%d%Y_%H%M%S")
        filename = '/img/'+date_time+'.jpg'
	# TODO Find out why this throws no file or directpry error
        self.__camera.capture(filename)
        self.__camera.stop_preview()
        self.__last_img = date_time
        return filename

    def read_temp_humid(self):
        '''
        Returns the temprature and humidity reading

        :return: temp, humid
        :rtype: float
        '''
        temp = self.__sht.read_temp()
        humid = self.__sht.read_humid()
        return [ temp, humid ]

    def read_float_switch(self):
        '''
        Returns the float switch state

        :return: state, 0 or 1
        :rtype: boolean, int
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__Float_sw, GPIO.IN)
        state = GPIO.input(self.__Float_sw)
        GPIO.cleanup()
        return state # HIGH (1) means empty, LOW (0) means full
    
    def measure(self):
        '''
        Runs the measurements and capture
        it to a dictionary
        '''
        date_time = datetime.now()
        data = {
            "date"          : date_time.strftime("%m-%d-%Y"),
            "timestamp"     : date_time.strftime("%H:%M:%S"),
            "soil_moisture" : self.read_moisture_levels(),
            "temp_humid"    : self.read_temp_humid(),
            "float_switch"  : self.read_float_switch(),
            #"img"           : self.capture_image(),
        }
        self.__data = data

    
    def return_last_img_name(self):
        '''
        Returns the last img filename

        :return: filename
        :rtype: str
        '''
        return self.__last_img

    def return_data(self):
        '''
        Returns the data as a dictionary

        :return: data
        :rtype: dict
        '''
        return self.__data

    def return_json(self):
        '''
        Returns the data as a json object

        :return: data
        :rtype: json
        '''
        json_object = json.dumps(self.__data, indent=4)
        return json_object

