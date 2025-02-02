from machine import Pin, PWM
from time import sleep
import random as rd


# 事前計算した定数
MIN_DUTY = 500 * 65535 // 20000  # 500μsを16ビットスケールで
MAX_DUTY = 2400 * 65535 // 20000  # 2400μsを16ビットスケールで
DUTY_RANGE = MAX_DUTY - MIN_DUTY  # 差分を定数として計算


def angle_to_duty(angle):
    # 角度をデューティー比に変換する関数
    return int(MIN_DUTY + DUTY_RANGE * angle // 180)


def sign(x):
    return (x > 0) - (x < 0)


class Ear:
    START = 0
    ACTION = 1
    WAIT = 2
    MOVE = 3
    MOTION = [80, 100, 80, 100, 80, 100, 90]

    def __init__(self, pin):
        self.pin = pin
        self.cangle = 0.0
        self.acc = 0.1
        self.wait = 0
        self.time = 0
        self.acenter = 90.0
        self.angle = self.acenter
        self.cangle = self.acenter
        self.amin = 60.0
        self.amax = 120.0
        self.wmin = 100
        self.wmax = 500
        self.step = self.START
        self.servo_pin = Pin(pin)
        self.servo = PWM(self.servo_pin)
        self.servo.freq(50)  # サーボモーターは50Hzで制御
        self.servo.duty_u16(angle_to_duty(self.acenter))

    def kick(self):
        if len(self.MOTION) <= self.time:
            return True
        self.angle = self.MOTION[self.time]
        print(self.angle)
        self.time += 1
        return False

    def idle(self):
        if self.step == self.START:
            self.angle = self.acenter
            self.cangle = self.acenter
            self.step = self.WAIT
        elif self.step == self.ACTION:
            self.time = 0
            self.step = self.MOVE
            self.kick()
        elif self.step == self.MOVE:
            s = sign(self.angle - self.cangle)
            d = abs(self.angle - self.cangle)*self.acc
            if d > 1.0:
                d = 1.0
            if d < 0.1:
                if self.kick():
                    self.step = self.WAIT
            self.cangle += d*s
        self.servo.duty_u16(angle_to_duty(self.cangle))

    def start(self):
        self.step = self.ACTION

    def action(self):
        return self.step == self.WAIT


class Head:
    START = 0
    NEXT = 1
    WAIT = 2
    ACTION = 3
    MOVE = 4
    ACTION_WAIT = 5

    def __init__(self, pin, ear):
        self.pin = pin
        self.cangle = 0.0
        self.acc = 0.1
        self.wait = 0
        self.acenter = 90.0
        self.angle = self.acenter
        self.cangle = self.acenter
        self.amin = 60.0
        self.amax = 120.0
        self.wmin = 100
        self.wmax = 500
        self.step = self.START
        self.servo_pin = Pin(pin)
        self.servo = PWM(self.servo_pin)
        self.servo.freq(50)  # サーボモーターは50Hzで制御
        self.servo.duty_u16(angle_to_duty(self.acenter))
        self.ear = ear

    def kick(self):
        self.wait = rd.randint(self.wmin, self.wmax)
        self.angle = rd.uniform(self.amin, self.amax)
        if rd.randint(0, 2) == 0:
            self.angle = self.acenter
        # print(self.step, self.wait, self.angle)

    def idle(self):
        if self.step == self.START:
            self.angle = self.acenter
            self.cangle = self.acenter
            self.step = self.NEXT
        elif self.step == self.NEXT:
            t = [self.WAIT, self.WAIT, self.WAIT, self.WAIT, self.ACTION, self.MOVE,
                 self.MOVE, self.MOVE, self.MOVE, self.MOVE, self.MOVE, self.MOVE, self.MOVE]
            n = rd.randint(0, len(t)-1)
            self.step = t[n]
            if self.step >= self.MOVE:
                self.step = self.MOVE
            if self.step == self.ACTION:
                print("action")
                self.ear.start()
            self.kick()
        elif self.step == self.MOVE:
            s = sign(self.angle - self.cangle)
            d = abs(self.angle - self.cangle)*self.acc
            if d > 1.0:
                d = 1.0
            if d < 0.1:
                self.step = self.NEXT
            self.cangle += d*s
            # print(self.cangle, self.angle)
        elif self.step == self.WAIT:
            self.wait -= 1
            if self.wait <= 0:
                self.step = self.NEXT
        elif self.step == self.ACTION:
            if self.ear.action():
                self.step = self.NEXT
        self.servo.duty_u16(angle_to_duty(self.cangle))


def main():
    sv0 = Ear(1)
    sv1 = Head(0, sv0)
    sleep(3)

    while True:
        sv0.idle()
        sv1.idle()
        sleep(0.015)


main()
