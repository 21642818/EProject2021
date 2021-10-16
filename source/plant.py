import time
import os
import json
import numpy as np
import RPi.GPIO as GPIO
from datetime import datetime
from ADC import ADCPi
from sht20 import SHT20
from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2

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

        #initialize Temp&Hum sensor
        self.__sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)

        # TODO read levels data from file
        file = open("moisture_levels_trigger.txt")
        try:
            trigger_levels = file.read().split('\n')
        finally:
            file.close()
        self.__trigger_levels = [float(trigger_levels[0]), float(trigger_levels[1]), float(trigger_levels[2]), float(trigger_levels[3])]
        print(self.__trigger_levels)

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

    def set_pump(self, relay_channels, duration=1):
        '''
        Sets the relays to high or low for a duration

        :param relay_channel: 1 to 4
        :type relay_channel: int
        :param duration: seconds, defaults to 1
        :type duration: int
        '''
        __valves_opened_flag = 0
        for r in range(4):
            __valves_opened_flag = __valves_opened_flag | relay_channels[r]
        
        # TODO Replace time.sleep with something else. This halts the program and we don't want it
        if __valves_opened_flag:
            if True: #self.read_float_switch == 0:
                self.gpio_init()
                for r in range(4):
                    GPIO.output(self.get_relay(r), relay_channels[r])
                GPIO.output(self.get_relay(4), GPIO.HIGH)
                time.sleep(duration)
                GPIO.output(self.get_relay(4), GPIO.LOW)
                for r in range(4):
                    GPIO.output(self.get_relay(r), GPIO.LOW)
                GPIO.cleanup()
                return True
            else:
                print("Error: water level is too low")
                return False
        return True
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
        #print(voltage)
        #offset = self.__adc_offset[channel - 1]
        #level = ((5.060569 - voltage)/(5.060569 - offset) ) * 100
        level = (5.060569-voltage) * 10
        return round(level, 3)

    def read_moisture_levels(self):
        '''
        Returns array of moisture levels from ADC channels 1 to 4
        in the format [ channel_1, channel_2, channel_3, channel_4]

        :return: moisture of channels
        :rtype: list
        '''
        pump = [0,0,0,0]
        moisture_levels = [self.get_moisture(1), self.get_moisture(2), self.get_moisture(3), self.get_moisture(4)]
        for x in range(4):
            if moisture_levels[x] < self.__trigger_levels[x]:
                pump[x] = 1
        self.set_pump(pump, 1)
        return [self.get_moisture(1), self.get_moisture(2), self.get_moisture(3), self.get_moisture(4)]

    def capture_image(self):
        '''
        Captures image with timestamp to './img/' and returns the filename

        :return: filename
        :rtype: string
        '''
        date_time=datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = 'img/'+date_time+'.jpg'
        #initialize Camera
        with PiCamera() as camera:
            try:
                camera.resolution = (3280, 2464)
                rawCapture = PiRGBArray(camera)
                # allow the camera to warmup
                time.sleep(0.1)
                # grab an image from the camera
                camera.capture(rawCapture, format="bgr")
                camera.stop_preview()
            finally:
                camera.close()
            image = rawCapture.array
            status = cv2.imwrite(filename, image)
            cv2.waitKey(1)
            if not status:
                raise Exception("Error: image '{}' did not save".format(filename))
        return filename, date_time

    def read_temp_humid(self):
        '''
        Returns the temprature and humidity reading

        :return: temp, humid
        :rtype: float
        '''
        temp = round(self.__sht.read_temp(), 2)
        humid = round(self.__sht.read_humid(), 2)
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
        return 0 #state # HIGH (1) means empty, LOW (0) means full

    def measure(self):
        '''
        Runs the measurements and capture
        it to a dictionary
        '''
        hour = datetime.now().hour
        if (hour > 8) and (hour < 20) : 
            file, img = self.capture_image()
        else :
            file = None
            img = None
        date_time = datetime.now()
        data = {
            "date"          : date_time.strftime("%Y-%m-%d"),
            "timestamp"     : date_time.strftime("%H:%M:%S"),
            "soil_moisture" : self.read_moisture_levels(),
            "temp_humid"    : self.read_temp_humid(),
            "float_switch"  : self.read_float_switch(),
            "img_path"      : file,
            "img"           : img,
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

    def water(self, pumps=[0,0,0,0], duration = 1, trigger_levels=[] ):
        '''
        Waters the plants by turning on the valves for a duration of time
        
        :param pumps: array of 4
        :type pumps: int array
        :param duration: seconds
        :type duration: int
        '''
        trigger_change_flag = False
        try:
            for i in range(4):
                if self.__trigger_levels[i] != trigger_levels[i]:
                    trigger_change_flag = True
                    break
        except:
            print("No triggers added")
        if trigger_change_flag:
            with open("moisture_levels_trigger.txt", 'w') as f:
                for line in trigger_levels:
                    f.write(line)
                    f.write('\n')
        self.__trigger_levels = trigger_levels
        return self.set_pump(pumps,duration)

