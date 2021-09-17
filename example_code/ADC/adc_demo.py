from ADC import *

def main():
    '''
    Main program function
    '''

    adc = ADCPi(0x68, 14)

    while True:

        # clear the console
        os.system('clear')

        # read from adc channels and print to screen
        print("Channel 1: %02f" % adc.read_voltage(1))
        print("Channel 2: %02f" % adc.read_voltage(2))
        print("Channel 3: %02f" % adc.read_voltage(3))
        print("Channel 4: %02f" % adc.read_voltage(4))
        # wait 1 seconds before reading the pins again
        time.sleep(1)

if __name__ == "__main__":
    main()

