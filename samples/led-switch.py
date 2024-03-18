#
# ボタン押下で LED オン、オフ
#
from machine import Pin
import time

button = Pin(16, Pin.IN, Pin.PULL_DOWN)
led = Pin(25, Pin.OUT)

while True:
    if button.value():
        led.toggle()
        time.sleep(0.5)
