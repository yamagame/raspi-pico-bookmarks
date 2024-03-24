#
# UDP パケット受信
# 参考: https://github.com/bokunimowakaru/pico/blob/master/examples/example05_lcd_udp.py
#
import network                                  # ネットワーク通信
import socket                                   # ソケット通信
from utime import sleep

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード

port = 1024                                     # UDPポート番号
buf_n = 128                                      # 受信バッファ容量(バイト)

wlan = network.WLAN(network.STA_IF)             # 無線LAN用のwlanを生成
wlan.active(True)                               # 無線LANを起動
wlan.connect(SSID, PASS)                        # 無線LANに接続
while not wlan.isconnected():                   # 接続待ち
    print('.', end='')                          # 接続中表示
    sleep(1)                                    # 1秒間の待ち時間処理
print(wlan.ifconfig()[0])                       # IPアドレスを表示

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ソケットを作成
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # オプション
    sock.bind(('', port))                        # ソケットに接続
except Exception as e:                          # 例外処理発生時
    while True:
        print(e)                                # エラー内容を表示
        sleep(3)                                # 3秒の待ち時間処理

while sock:                                     # 永遠に繰り返す
    udp, udp_from = sock.recvfrom(buf_n)        # UDPパケットを取得
    udp = udp.decode()                          # UDPデータを文字列に変換
    s = ''                                        # 表示用の文字列変数s
    for c in udp:                               # UDPパケット内
        if ord(c) >= ord(' ') and ord(c) <= ord('~'):  # 表示可能文字
            s += c                              # 文字列sへ追加
    print(udp_from[0] + ', ' + s)               # 受信データをシリアル出力
sock.close()                                    # ソケットの切断
