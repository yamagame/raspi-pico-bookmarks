#
# アナログ値でLED制御
#
from machine import Pin, PWM
import math
import time

LED_PIN = 'GP5'
PWM_PIN = 'GP16'
ADC0_PIN = 0  # GP26(31番ピン)

pwm = machine.PWM(machine.Pin(LED_PIN))
pwm.freq(100)

sensor_adc = machine.ADC(ADC0_PIN)


def brightness(analog):
    return int(math.pow((analog / 65535), 3) * 65535)


while True:
    pwm.duty_u16(brightness(sensor_adc.read_u16()))
