#
# I2C OLEDサンプル
#
from machine import I2C, Pin
from utime import sleep
import ssd1306

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.rect(10, 0, 100, 18, 1)
oled.show()
oled.text("Hello World!", 13, 5)
oled.show()

n = 0

while True:
    oled.fill_rect(20, 40, 30, 10, 0)
    oled.show()
    oled.text(str(n), 20, 40)
    oled.show()
    n = n+1
    sleep(1)
