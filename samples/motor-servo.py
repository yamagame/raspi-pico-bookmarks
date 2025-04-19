#
# ラズベリーパイ・ラズベリーパイPicoでサーボ―モーターの使い方
# https://raspi-school.com/servo/
#
from machine import PWM, Pin
from time import sleep

PWM_PIN = 16

servo = PWM(Pin(PWM_PIN))
servo.freq(50)


def angle(degree):
    return int((degree * 0.097 / 180 + 0.025) * 65535)


while True:
    servo.duty_u16(angle(0))
    sleep(1)
    servo.duty_u16(angle(90))
    sleep(1)
    servo.duty_u16(angle(180))
    sleep(1)
    servo.duty_u16(angle(90))
    sleep(1)
