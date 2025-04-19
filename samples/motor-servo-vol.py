#
# ラズベリーパイ・ラズベリーパイPicoでサーボ―モーターの使い方
# https://fujimoostudios.org/?p=204
#
from machine import Pin, PWM

PWM_PIN = 'GP16'
ADC0_PIN = 0  # GP26(31番ピン)

pwm = PWM(Pin(PWM_PIN))
pwm.freq(50)

sensor_adc = machine.ADC(ADC0_PIN)


def angle(degree):
    return int((degree * 0.097 / 180 + 0.025) * 65535)


while True:
    pwm.duty_u16(angle(sensor_adc.read_u16() * 180 / 65535))
