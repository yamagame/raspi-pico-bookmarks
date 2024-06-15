#
# DC Motor/Fan Speed Controller with Raspberry Pi Pico
# https://how2electronics.com/dc-motor-fan-speed-controller-with-raspberry-pi-pico/
#
from machine import Pin, ADC, PWM
from time import sleep

MOT_PIN = 16                 # L9110S Motor Drive Module
POT_PIN = 0                  # ADC0 multiplexing pin is GP26


def setup():
    global A_1A
    global pot_ADC

    A_1A = PWM(Pin(MOT_PIN))
    A_1A.freq(1000)  # Set the driver operating frequency to 1K
    pot_ADC = ADC(POT_PIN)


def loop():
    while True:
        print('Potentiometer Value:', pot_ADC.read_u16())
        Value = pot_ADC.read_u16()
        A_1A.duty_u16(Value)             # control fan speed
        sleep(0.2)


if __name__ == '__main__':
    setup()
    loop()
