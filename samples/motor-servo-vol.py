#
# ラズベリーパイ・ラズベリーパイPicoでサーボ―モーターの使い方
# https://fujimoostudios.org/?p=204
#
from machine import Pin, PWM

PWM_PIN = 16
ADC0_PIN = 0  # GP26(31番ピン)

pwm = PWM(Pin(PWM_PIN))
pwm.freq(50)

sensor_adc = machine.ADC(ADC0_PIN)


def servo_value(degree):
    return int((degree * 9.5 / 180 + 2.5) * 65535 / 100)


while True:
    pwm.duty_u16(servo_value(sensor_adc.read_u16() * 180 / 65535))
