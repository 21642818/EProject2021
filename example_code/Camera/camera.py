# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import cv2

def take_photo():
    date_time = datetime.now().strftime("%m%d%Y-%H%M%S")
    filename = 'img/'+date_time+'.jpg'
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (2048, 1536)
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    camera.close_preview()
    camera.close()
    image = rawCapture.array
    # display the image on screen and wait for a keypress
    status = cv2.imwrite(filename, image)
    cv2.waitKey(0)
    print (status)

take_photo()
time.sleep(10)
take_photo()

