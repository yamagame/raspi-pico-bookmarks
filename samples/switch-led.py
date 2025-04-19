from machine import Pin
import time

SW_PIN = 'GP21'

LED_PIN = 'GP5'

led = machine.Pin(LED_PIN, machine.Pin.OUT)

sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

while True:
    if sw.value():
        led.value(0)
    else:
        led.value(1)
