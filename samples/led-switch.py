#
# ボタン押下で LED オン、オフ
#
from machine import Pin
import time

BTN_PIN = 16
LED_PIN = 'LED'

button = Pin(BTN_PIN, Pin.IN, Pin.PULL_DOWN)
led = Pin(LED_PIN, Pin.OUT)

while True:
    if button.value():
        led.toggle()
        time.sleep(0.5)
