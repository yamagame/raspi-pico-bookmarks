from machine import I2C, Pin
from urtc import DS1307
import utime

# i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
rtc = DS1307(i2c)

LED_PIN = 'LED'
led = Pin(LED_PIN, Pin.OUT)

# year = int(input("Year : "))
# month = int(input("month (Jan --> 1 , Dec --> 12): "))
# date = int(input("date : "))
# day = int(input("day (1 --> monday , 2 --> Tuseday ... 0 --> Sunday): "))
# hour = int(input("hour (24 Hour format): "))
# minute = int(input("minute : "))
# second = int(input("second : "))

# now = (year, month, date, day, hour, minute, second, 0)
# rtc.datetime(now)

while True:
    utime.sleep(1)
    led.toggle()
    (year, month, date, day, hour, minute, second, p1) = rtc.datetime()
    print(rtc.datetime())
