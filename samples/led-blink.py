#
# LED がホタルのように明滅
#
import machine
import utime

pwm = machine.PWM(machine.Pin('LED'))
pwm.freq(100)
x = 0.5
dx = 0.01

while True:
    if x < 0.01 or x > 0.95:
        dx = -dx
    x = x + dx
    pwm.duty_u16(int(65535*x))
    utime.sleep(0.02)
