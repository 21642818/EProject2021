from sht20 import SHT20
from time import sleep

sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)

# or

data = sht.read_all()
temp = data[0]
humid = data[1]

print ("Temperature (*C): " + str(temp))
print ("Humidity (%RH): " + str(humid))
