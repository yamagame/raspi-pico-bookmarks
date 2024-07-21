from machine import I2C, PWM, Pin, Timer
from urtc import DS1307
import ssd1306
import utime
import time

WIDTH = 128
HEIGHT = 64

RED_LED = 10
BLUE_LED = 11
PWM_PIN = 20
SW_PIN = 21
LED_PIN = 'LED'

active = True
next_action_seconds = 10

blue_led = Pin(BLUE_LED, Pin.OUT)
red_led = Pin(RED_LED, Pin.OUT)
sw = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)
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

melody = [D5, E5, 0, D5, E5, 0, C6, B5, 0, 0, G5]
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


def checkbutton(timestamp):
    global beat_i
    global active
    pushedtime = read_eeprom(14)
    if int(pushedtime)+next_action_seconds < int(timestamp):
        active = False
    if not active and sw.value() == 0:
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
    print(timestamp, pushedtime)
