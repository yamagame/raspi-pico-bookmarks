#
# TCP クライアント
# 参考: https://github.com/bokunimowakaru/pico/blob/master/examples/tcp_htget_u.py
#
from sys import exit                        # ライブラリsysからexitを組み込む
import ujson                                # JSON変換ライブラリを組み込む
import usocket                              # ソケット通信ライブラリ
import network                              # ネットワーク通信ライブラリ
from utime import sleep

SSID = "1234ABCD"                           # 無線LANアクセスポイント SSID
PASS = "password"                           # パスワード

host_s = 'bokunimo.net'                     # アクセス先のホスト名
path_s = '/iot/cq/test.json'                # アクセスするファイルパス

wlan = network.WLAN(network.STA_IF)             # 無線LAN用のwlanを生成
wlan.active(True)                               # 無線LANを起動
wlan.connect(SSID, PASS)                        # 無線LANに接続
while wlan.status() != 3:                       # 接続待ち
    print('.', end='')                          # 接続中表示
    sleep(1)                                    # 1秒間の待ち時間処理
print('\n', wlan.ifconfig())                     # 無線LANの状態を表示

addr = usocket.getaddrinfo(host_s, 80)[0][-1]
sock = usocket.socket()
sock.connect(addr)
req = 'GET ' + path_s + ' HTTP/1.0\r\n'
req += 'Host: ' + host_s + '\r\n\r\n'
sock.send(bytes(req, 'UTF-8'))

body = '<head>'
while True:
    res = str(sock.readline(), 'UTF-8')
    print(res.strip())
    if len(res) <= 0:
        break
    if res == '\n' or res == '\r\n':
        body = '<body>'
        break
if body != '<body>':
    print('no body data')
    sock.close()
    exit()

body = ''
while True:
    res = str(sock.readline(), 'UTF-8').strip()
    if len(res) <= 0:
        break
    body += res

print(body)

res_dict = ujson.loads(body)      # 受信データを変数res_dictへ代入
# -----------------------------
print('--------------------------------------')
print('title :', res_dict.get('title'))         # 項目'title'の内容を取得・表示
print('descr :', res_dict.get('descr'))         # 項目'descr'の内容を取得・表示
print('state :', res_dict.get('state'))         # 項目'state'の内容を取得・表示
print('url   :', res_dict.get('url'))           # 項目'url'内容を取得・表示
print('date  :', res_dict.get('date'))          # 項目'date'内容を取得・表示

sock.close()                                # ソケットの終了
