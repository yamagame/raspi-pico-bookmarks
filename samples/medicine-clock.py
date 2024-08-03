from machine import I2C, PWM, Pin, Timer
from urtc import DS1307
import re
import time
import datetime
import ssd1306
import utime

WIDTH = 128
HEIGHT = 64

RED_LED = 7  # 10
BLUE_LED = 8  # 11
PWM_PIN = 20
SW_PIN = 21
LED_PIN = 'LED'
MOD_PIN = 16

SW_ON = 0

active = True

blue_led = Pin(BLUE_LED, Pin.OUT)
red_led = Pin(RED_LED, Pin.OUT)
sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)
mod = Pin(MOD_PIN, Pin.IN, Pin.PULL_UP)
led = Pin(LED_PIN, Pin.OUT)
led.value(0)

i2c0 = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c0)
i2c1 = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
rtc = DS1307(i2c1)
eeeprom = i2c1


def write_eeprom(s):
    eeeprom.writeto_mem(0x50, 0x0F00, s.encode(), addrsize=16)
    time.sleep_ms(5)


def read_eeprom(len):
    try:
        return eeeprom.readfrom_mem(0x50, 0x0F00, len, addrsize=16).decode('utf-8', 'replace')
    except Exception as e:
        return "20000101000000"


speaker = PWM(Pin(PWM_PIN, Pin.OUT))

A4 = 440
B4 = 493.883
C5 = 523.251
C5s = 554.365
D5 = 587.330
E5 = 659.255
F5 = 698.456
F5s = 739.989
G5 = 783.991
A5 = 880
B5 = 987.767
C6 = 1046.502

mspb = 156

melody = [D5, E5, 0, D5, E5, 0, D5, E5, 0, 0, G5]
beat_i = 0


def beat(timer):
    global melody
    global led_onboard
    global beat_i
    global speaker

    if beat_i >= len(melody):
        speaker.deinit()
        timer.deinit()

    elif int(melody[beat_i]) == 0:
        speaker.duty_u16(0)

    else:
        speaker.freq(int(melody[beat_i] + 0.5))
        speaker.duty_u16(0x8000)

    beat_i += 1


timestamp = ""


def parsetime(timestamp):
    r = re.match('(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)', timestamp)
    if r:
        year = int(r.group(1))
        month = int(r.group(2))
        day = int(r.group(3))
        hour = int(r.group(4))
        minute = int(r.group(5))
        second = int(r.group(6))
        return datetime.datetime(
            year=year, month=month, day=day,
            hour=hour, minute=minute, second=second
        )


def addtime(dt1, deltasec):
    if dt1:
        dt2 = datetime.timedelta(seconds=deltasec)
        dt3 = dt1 + dt2
        return "{0:04}{1:02}{2:02}{3:02}{4:02}{5:02}".format(
            dt3.year, dt3.month, dt3.day,
            dt3.hour, dt3.minute, dt3.second
        )
    return "0"


def nexttime(pushedtime):
    is_debug = mod.value() == SW_ON
    if is_debug:
        # デバッグモードは10秒でタイムアウト
        return addtime(parsetime(pushedtime), 10)
    # 次の日の朝5時まで
    t = parsetime(pushedtime)
    t = datetime.datetime(year=t.year, month=t.month, day=t.day)
    return addtime(t, (24+5)*60*60)


def checkbutton(timestamp):
    global beat_i
    global active
    pushedtime = read_eeprom(14)
    if int(nexttime(pushedtime)) < int(timestamp):
        active = False
    if not active and sw.value() == SW_ON:
        active = True
        tim = Timer()
        beat_i = 0
        tim.init(period=mspb, mode=Timer.PERIODIC, callback=beat)
        write_eeprom(timestamp)
    if active:
        blue_led.value(1)
        red_led.value(0)
    else:
        blue_led.value(0)
        red_led.value(1)
    return pushedtime


while True:
    utime.sleep(0.5)
    try:
        (year, month, date, day, hour, minute, second, p1) = rtc.datetime()
        oled.fill_rect(0, 0, WIDTH, HEIGHT, 0)
        datestr = "{0:04}/{1:02}/{2:02}".format(year, month, date)
        timestamp = "{0:04}{1:02}{2:02}{3:02}{4:02}{5:02}".format(
            year, month, date, hour, minute, second)
        oled.text(datestr, 24, 20)
        timestr = "{0:02}:{1:02}:{2:02}".format(hour, minute, second)
        oled.text(timestr, 32, 36)
        oled.show()
        # print(rtc.datetime())
    except OSError as e:
        print('catch OSError:', e)
    checkbutton(timestamp)
    utime.sleep(0.5)
    pushedtime = checkbutton(timestamp)
    print(timestamp, pushedtime, nexttime(pushedtime))
