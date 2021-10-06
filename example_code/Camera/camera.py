from picamera import PiCamera
from time import sleep
import numpy as np
import cv2
from fractions import Fraction
from datetime import datetime

with PiCamera() as camera:
    camera.resolution = (3280, 2464)
    camera.start_preview()
    sleep(2)
    #now = datetime.now()
    #d = now.strftime("%m%d%Y_%H%M%S")
    filename = './img/'+datetime.now().strftime("%m%d%Y-%H%M%S")+'.png'
    #camera.capture('./img/'+datetime.now().strftime("%m%d%Y_%H%M%S")+'.jpg')
    image = np.empty((2464 * 3280 * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((2464, 3280, 3))
    status = cv2.imwrite(filename, image)
    print(status)
    camera.stop_preview()
