from machine import Pin
import time

SW_PIN = 0

sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

while True:
    print(sw.value())
    time.sleep(0.5)
