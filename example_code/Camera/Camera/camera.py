from picamera import PiCamera
from time import sleep
from fractions import Fraction

camera = PiCamera(resolution = (3280, 2464),
		sensor_mode=2)
camera.start_preview()
sleep(5)
camera.capture('./image.jpg')
camera.stop_preview()
