from smbus import SMBus
import re
import platform
import time

class SHT20(object):
    """
    Control the SHT20 module through Python
    """
    # internal variables
    __adc_adress = 0x40

    __adc_conf = 