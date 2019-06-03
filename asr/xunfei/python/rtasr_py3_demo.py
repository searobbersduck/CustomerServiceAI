# !/usr/bin/env python3

import base64
import hashlib
import hmac
import json
import os
import time
import requests
from websocket import create_connection
import threading
from urllib.parse import quote

rtasr_host = 'ws://rtasr.xfyun.cn/v1/ws'
app_id = "5be0fbcb"
api_key = "9502d486f048d76978099f0646fe4f52"
# file_path = "./test_1.pcm"
file_path = '/Users/higgs/beast/data/audio/兔司机与候选人首次沟通录音/0f73049d-c131-4b83-b7f0-c73a34eea77c.wav'
end_tag = "{\"end\": true}"

class Client:
    def __init__(self, appid, secret_key):
        self.appid = appid
        self.secret_key = secret_key
        ts = str(int(time.time()))
        m2 = hashlib.md5()
        m2.update((appid+ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.ws = create_connection(rtasr_host + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv())
        self.trecv.start()

    def send(self, file_path):
        with open(file_path, 'rb') as f:
            try:
                index = 1
                while True:
                    chunk = f.read(1280)
                    if not chunk:
                        break
                    self.ws.send(chunk)
                    index += 1
                    time.sleep(0.04)
            finally:
                pass
        self.ws.send(bytes(end_tag))

    def recv(self):
        while self.ws.connected:
            result = str(self.ws.recv())
            print(result)

if __name__ == '__main__':
    client = Client(app_id, api_key)
    client.send(file_path)