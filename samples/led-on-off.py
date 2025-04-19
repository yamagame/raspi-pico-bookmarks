#
# LED が 1 秒ごとに点滅
#
import machine
import utime

LED_PIN = 'GP5'

led = machine.Pin(LED_PIN, machine.Pin.OUT)

while True:
    led.value(1)
    utime.sleep(1)
    led.value(0)
    utime.sleep(1)
