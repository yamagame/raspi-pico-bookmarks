#
# ボタン押下で LED オン、オフ
#
from machine import Pin
import time

SW_PIN = 'GP21'

LED_PIN = 'GP5'

led = machine.Pin(LED_PIN, machine.Pin.OUT)

sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)
prevsw = sw.value()

while True:
    swval = sw.value()
    if prevsw != swval and swval:
        led.toggle()
    prevsw = swval
    time.sleep(0.1)
