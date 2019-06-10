#-*- encoding:utf-8 -*-

import sys
import hashlib
from hashlib import sha1
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib import quote
import logging
import fire
import os

reload(sys)
sys.setdefaultencoding("utf8")
logging.basicConfig()

'''
usage: python parse_audio_rt.py paser_audio_rt $infile $outdir
'''

base_url = "ws://rtasr.xfyun.cn/v1/ws"
app_id = "5be0fbcb"
api_key = "9502d486f048d76978099f0646fe4f52"
end_tag = "{\"end\": true}"

sentences = []
streams = []

def parse_rt_json(s_json):
    '''
    :param s_json: string
    :return:
    '''
    # res_dict = json.loads(s_json)
    res_dict = s_json
    action = res_dict["action"]
    sent = ''
    if action == 'result':
        data = res_dict['data']
        data_dict = json.loads(data)
        rt_list = data_dict['cn']['st']['rt']
        sign_flag = False
        if int(data_dict['cn']['st']['type']) == 0:
            first = True
            for rt in rt_list:
                ws_list = rt['ws']
                sent = ''
                for ws in ws_list:
                    if first:
                        sign_flag = ws['cw'][0]['wp'] = 'p'
                        first = False
                    sent += ws['cw'][0]['w']
                # print(sent)
    if sent != '':
        # if sign_flag:
        #     if len(sentences) >= 1:
        #         sentences[-1] = sentences[-1]+sent[0]
        #         sentences.append(sent[1:])
        #         print(sentences[-1])
        #     else:
        #         sentences.append(sent)
        #         print(sent)
        # else:
        #     sentences.append(sent)
        #     print(sent)
        sentences.append(sent)
        print(sent)
    return action, sent

class Client():
    def __init__(self):
        # 生成鉴权参数
        ts = str(int (time.time()))
        tmp = app_id + ts
        hl = hashlib.md5()
        hl.update(tmp.encode(encoding='utf-8'))
        my_sign = hmac.new(api_key,  hl.hexdigest(), sha1).digest()
        signa = base64.b64encode(my_sign)

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send(self, file_path):
        file_object = open(file_path, 'rb')
        try:
            index = 1
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                self.ws.send(chunk)

                index += 1
                time.sleep(0.04)
        finally:
            # print str(index) + ", read len:" + str(len(chunk)) + ", file tell:" + str(file_object.tell())
            file_object.close()

        self.ws.send(bytes(end_tag))
        print "send end tag success"

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print "receive result end"
                    break
                result_dict = json.loads(result)

                # 解析结果
                if result_dict["action"] == "started":
                    print "handshake success, result: " + result

                if result_dict["action"] == "result":
                    parse_rt_json(result_dict)
                    streams.append(result_dict)
                    # print "rtasr result: " + result

                if result_dict["action"] == "error":
                    print "rtasr error: " + result
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print "receive result end"

    def close(self):
        self.ws.close()
        print "connection closed"

def paser_audio_rt(infile, outdir):
    print('\n')
    print('====> begin processing {}'.format(infile))
    print('output directory: {}'.format(outdir))
    client = Client()
    client.send(infile)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    basename = os.path.basename(infile).split('.')[0]+'.txt'
    basename_ss = os.path.basename(infile).split('.')[0]+'.json'
    with open(os.path.join(outdir, basename), 'w') as f:
        f.write('\n'.join(sentences))
        print('write {} sentences'.format(len(sentences)))
    with open(os.path.join(outdir, basename_ss), 'w') as f:
        f.write(json.dumps(streams))
    print('====> end!')
    print('\n')

if __name__ == '__main__':
    fire.Fire()
