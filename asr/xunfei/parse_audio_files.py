# !/usr/bin/env python3

import os
from glob import glob
import fire
import json

from weblfasr_python3_demo import *

appid = "5cedf2a9"
secret_key="1ce47074ecb5262970bd505e733dad06"

# appid = "5cee3974"
# secret_key="c81d93def5d2bf270e606a8cace2acf4"

def parse_audio_files_wav(indir, outfile):
    audio_files = glob(os.path.join(indir, '*.wav'))
    res_dict = {}
    total_count = len(audio_files)
    cnt = 0
    try:
        for file in audio_files:
            cnt += 1
            key_name = os.path.basename(file)
            api = RequestApi(appid=appid, secret_key=secret_key,
                             upload_file_path=file)
            res = api.all_api_request()
            res_dict[key_name] = res
            print('====> [{}/{}] finished!'.format(cnt, total_count))
            print('\n\n')
    except:
        pass
    with open(outfile, 'w', encoding='utf8') as f:
        f.write(json.dumps(res_dict, ensure_ascii=False))

def parse_wav_audio(infile, outfile):
    res_dict = {}
    key_name = os.path.basename(infile)
    api = RequestApi(appid=appid, secret_key=secret_key,
                     upload_file_path=infile)
    res = api.all_api_request()
    res_dict[key_name] = res
    with open(outfile, 'w', encoding='utf8') as f:
        f.write(json.dumps(res_dict, ensure_ascii=False))

if __name__ == '__main__':
    fire.Fire()