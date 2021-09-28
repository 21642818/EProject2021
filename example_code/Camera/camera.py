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
camera.capture('./img/'+datetime.now().strftime("%m%d%Y_%H%M%S")+'.jpg')
#sleep(2)
#camera.capture('./img/'+datetime.now().strftime("%m%d%Y_%H%M%S")+'_resize'+'.jpg', resize=(2592, 1944) )
camera.stop_preview()
