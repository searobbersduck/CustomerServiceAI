# !/usr/bin/env python3
import os
import shutil
from glob import glob
import subprocess
import fire

def multi_folders(indir, outdir, filenum_per_folder):
    wave_list = glob(os.path.join(indir, '*.wav'))
    folder_num = (len(wave_list)+filenum_per_folder-1)//filenum_per_folder
    command_list = []
    for i in range(folder_num):
        subdir = os.path.join(outdir, '{}'.format(i))
        os.makedirs(subdir, exist_ok=True)
        end_index = min(len(wave_list), (i+1)*filenum_per_folder)
        start_index = i*filenum_per_folder
        for file in wave_list[start_index:end_index]:
            src_file = file
            dst_file = os.path.join(subdir, os.path.basename(src_file))
            shutil.copyfile(src_file, dst_file)
            print('copy from {} to {}'.format(src_file, dst_file))
        command = './test.sh {} {}'.format(subdir, i)
        command_list.append(command)
    with open('task.sh', 'w') as f:
        f.write('\n'.join(command_list))

if __name__ == '__main__':
    fire.Fire()