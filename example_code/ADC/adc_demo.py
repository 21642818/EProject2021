import time
import os
from ADC import ADCPi

def main():
    '''
    Main program function
    '''

    adc = ADCPi(0x68, 18)
    adc.set_conversion_mode(0)
    adc_offset = [2.983771, 2.847210, 2.747443, 2.773041]
    os.system('clear')

    while True:
        print('*********************')
	# read from adc channels and print to screen
        print("Channel 1: %02f" % adc.read_voltage(1))
        print("Channel 2: %02f" % adc.read_voltage(2))
        print("Channel 3: %02f" % adc.read_voltage(3))
        print("Channel 4: %02f" % adc.read_voltage(4))
        # wait 1 seconds before reading the pins again
        voltage = adc.read_voltage(1)
        offset = adc_offset[0]
        level = ((5.060569 - voltage)/(5.060569 - offset) ) * 100
        if (level < 0.0) and (level > 100.0):
            level = None
        print (round(level, 2))

        time.sleep(5)

if __name__ == "__main__":
    main()

