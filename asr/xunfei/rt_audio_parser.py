# !/usr/bin/env python2
# -*- encoding:utf-8 -*-

import json

'''
{"action":"result","code":"0","data":"{\"cn\":{\"st\":{\"bg\":\"10\",\"ed\":\"1500\",\"rt\":[{\"ws\":[{\"cw\":[{\"w\":\"啊\",\"wp\":\"s\"}],\"wb\":12,\"we\":20},{\"cw\":[{\"w\":\"我\",\"wp\":\"n\"}],\"wb\":47,\"we\":72}]}],\"type\":\"0\"}},\"seg_id\":0}\n","desc":"success","sid":"rta002ae901@dx5e77104fcbcea12200"}
'''

s_example_action = {"action":"result","code":"0","data":"{\"cn\":{\"st\":{\"bg\":\"10\",\"ed\":\"1500\",\"rt\":[{\"ws\":[{\"cw\":[{\"w\":\"啊\",\"wp\":\"s\"}],\"wb\":12,\"we\":20},{\"cw\":[{\"w\":\"我\",\"wp\":\"n\"}],\"wb\":47,\"we\":72}]}],\"type\":\"0\"}},\"seg_id\":0}\n","desc":"success","sid":"rta002ae901@dx5e77104fcbcea12200"}

# 解析上述格式

def parse_rt_json(s_json):
    '''
    :param s_json: string
    :return:
    '''
    # res_dict = json.loads(s_json)
    res_dict = s_json
    action = res_dict["action"]
    if action == 'result':
        data = res_dict['data']
        data_dict = json.loads(data)
        rt_list = data_dict['cn']['st']['rt']
        if int(data_dict['cn']['st']['type']) == 0:
            for rt in rt_list:
                ws_list = rt['ws']
                sent = ''
                for ws in ws_list:
                    sent += ws['cw'][0]['w']
                print(sent)

if __name__ == '__main__':
    parse_rt_json(s_example_action)