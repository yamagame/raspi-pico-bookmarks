from machine import Pin, PWM, Timer
import time

PWM_PIN = 16
LED_PIN = 'LED'
SW1_PIN = 0
SW2_PIN = 1


speaker = PWM(Pin(PWM_PIN, Pin.OUT))  # スピーカーを接続しているGPIOを作成し、それをPWM()へ渡す
led_onboard = Pin(LED_PIN, Pin.OUT)  # 基板上のLEDを光らせたいのでGPIO25作成

# 使用する音の周波数を宣言しておく。ピタゴラスイッチは低いラ～高いドまでの音を使う
A4 = 440  # ラ
B4 = 493.883  # シ
C5 = 523.251  # ド
C5s = 554.365  # ド#
D5 = 587.330  # レ
E5 = 659.255  # ミ
F5 = 698.456  # ファ
F5s = 739.989  # ファ#
G5 = 783.991  # ソ
A5 = 880  # ラ
B5 = 987.767  # シ
C6 = 1046.502  # ド

# bps = 6.4 # 原曲128bpm / 60秒 = 2.1333...bps * 3連符 = 6.4bps
mspb = 156  # 6.4bpsの逆数 = 0.156ms　これが8分3連符ひとつ分の音の長さ、音の間隔となる


def play(notes):
    i = 0

    # 音を鳴らすためのコールバック関数
    def beat(timer):
        nonlocal i
        global speaker

        if i >= len(notes):  # メロディーを最後まで演奏し終えたら
            speaker.deinit()  # スピーカーのPWMを破棄して
            # led_onboard.value(0)  # LEDを消して
            timer.deinit()  # タイマーを破棄して終了
            i = 0

        elif int(notes[i]) == 0:  # メロディー音が0、つまり無音（休符）の場合
            speaker.duty_u16(0)  # PWMのDutyを0とすることで波形は出力されずLOWとなり、音は出ない
            # led_onboard.value(0)  # LEDを消す

        else:
            # PWMの周波数を次のメロディー音の周波数に変更する。整数で渡す必要があるので、+0.5してから小数点以下切り捨て（thanks @naohiro2g）
            speaker.freq(int(notes[i] + 0.5))
            # PWMのDutyを50％に戻し、音を出す。Dutyは0～0xFFFFつまり65535までの間の値で設定
            speaker.duty_u16(0x8000)
            # led_onboard.value(1)  # LEDを光らせる

        i += 1  # メロディーを次に進めて終わり

    tim = Timer()
    # 8分3連符の間隔でコールバックを呼ぶタイマーを作成し、メロディースタート
    tim.init(period=mspb, mode=Timer.PERIODIC, callback=beat)


class Button:
    def __init__(self, pin):
        self.pin = pin
        self.sw = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.push = False

    def idle(self, notes):
        v = self.sw.value()
        # print(v)
        if v == 0 and self.push == False:
            play(notes)
            self.push = True
            return True
        if v == 1 and self.push == True:
            self.push = False
        return False


sw1 = Button(SW1_PIN)
sw2 = Button(SW2_PIN)


# ドレミ
sound_doremi = [0, C5, D5, E5]
# ラソラ
sound_rasora = [0, A5, G5, A5]


while True:
    if sw1.idle(sound_doremi):
        led_onboard.value(1)  # LEDを光らせる
    if sw2.idle(sound_rasora):
        led_onboard.value(0)  # LEDを消す
    time.sleep(0.25)
