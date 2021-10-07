from picamera import PiCamera
from time import sleep
import numpy as np
import cv2
from fractions import Fraction
from datetime import datetime

with PiCamera() as camera:
    camera = PiCamera()
    camera.resolution = (3280, 2464)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('foo.jpg')
