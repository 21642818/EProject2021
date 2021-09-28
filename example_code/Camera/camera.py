from picamera import PiCamera
from time import sleep
from fractions import Fraction
from datetime import datetime

camera = PiCamera(resolution = (3280, 2464),
		sensor_mode=2)
camera.start_preview()
sleep(5)
#now = datetime.now()
#d = now.strftime("%m%d%Y_%H%M%S")
camera.capture('/img/{}.jpg'.format(datetime.now().strftime("%m%d%Y_%H%M%S")))
