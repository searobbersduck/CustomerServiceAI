# !/usr/bin/env python3
'''
将1个channel的文件提取出来
'''

import os
import subprocess
from glob import glob
import shutil
import fire
import re

def split_channels(indir, outdir):
    files = glob(os.path.join(indir, '*.wav'))
    os.makedirs(outdir,exist_ok=True)
    c1_dir = os.path.join(outdir, 'c1')
    c2_dir = os.path.join(outdir, 'c2')
    os.makedirs(c1_dir, exist_ok=True)
    os.makedirs(c2_dir, exist_ok=True)
    for file in files:
        res = subprocess.Popen('sox -V {} -n'.format(file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res_out = res.stdout.read()
        o1 = bytes.decode(res_out)
        pos = o1.find('channels')
        if pos > 2:
            channel_num = -1
            try:
                channel_num = int(o1[pos-2:pos-1])
            except:
                continue
        print('====> begin')
        if channel_num == 1:
            src_file = file
            dst_file = os.path.join(c1_dir, os.path.basename(src_file))
            shutil.copyfile(src_file, dst_file)
            print('copy from {} to {}'.format(src_file, dst_file))
        elif channel_num == 2:
            src_file = file
            dst_file = os.path.join(c2_dir, os.path.basename(src_file))
            shutil.copyfile(src_file, dst_file)
            print('copy from {} to {}'.format(src_file, dst_file))
        print('====> end')


if __name__ == '__main__':
    fire.Fire()