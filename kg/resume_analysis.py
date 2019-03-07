# !/usr/bin/env python3

import json
import os
from glob import glob

# 提取json文件中的key，以用来在数据库简历表格

infile = '/Users/higgs/beast/code/work/ResumeAnalyze/try/resume_analyze_basicinfo/tzhuopin_output/byHTML (1).html_json.txt'

re_create = 'create table if not exists `{}`(' \
     '`id` int unsigned auto_increment,' \
     '{},' \
     'primary key(`id`))ENGINE=InnoDB DEFAULT CHARSET=utf8;'

re_insert = """insert into {} ({}) values ('{0}', '{1}', {2})"""

dict_keys = {}

def get_mysql_type(t):
    if t == 'int':
        return 'int'
    elif t == 'str':
        return 'varchar(100)'
    else:
        return 'varchar(100)'

cmd_dict = {}

def extract_keys(infile):
    cmd_list = []
    with open(infile, encoding='utf8') as f:
        json_l = json.load(f)
        for l in json_l:
            print(l.keys())
            for key in l.keys():
                cont = l[key]
                cont = json.loads(cont)
                list_keys = []
                for kkey in cont.keys():
                    print('\t{}'.format(kkey))
                    print('\t\t{}'.format(type(cont[kkey]).__name__))
                    mysql_key = '`{}` {}'.format(kkey, get_mysql_type(type(cont[kkey]).__name__))
                    list_keys.append(mysql_key)
                    dict_keys[kkey] = 0
                mysql_keys = ','.join(list_keys)
                if key not in cmd_dict:
                    cmd_dict[key] = re_create.format(key, mysql_keys)
                print(mysql_keys)
            break
        print('hello world!')

extract_keys(infile)

print(cmd_dict)

print(cmd_dict['basic'])
# print(cmd_dict['education'])

# connect mysql database
import pymysql
addr = '172.16.52.70'
db = pymysql.connect(addr, 'test1', '111111')
cursor = db.cursor()
cursor.execute('create database if not exists resume')
db.commit()
cursor.execute('use resume')
cursor.execute(cmd_dict['basic'])
# cursor.execute(cmd_dict['education'])
db.commit()


def extract_single_info_to_mysql(cursor, infile):
    with open(infile, encoding='utf8') as f:
        json_cont = json.load(f)
        for l in json_cont:
            for key in l.keys():
                if not (key == 'basic'):
                    continue
                info = l[key]
                info = json.loads(info)
                list_keys = []
                k_list = []
                v_list = []
                v_keys = """"""
                for kkey in info.keys():
                    if kkey not in dict_keys:
                        continue
                    if True:
                        k_list.append(kkey)
                        v_list.append(info[kkey])
                        if type(info[kkey]).__name__ == 'int':
                            v_keys = v_keys + "{}".format(info[kkey])
                        elif type(info[kkey]).__name__ == 'str':
                            v_keys = v_keys + "'{}'".format(info[kkey])
                        v_keys  = v_keys + ""","""
                v_keys = v_keys[:-1]
                k_keys = ','.join(k_list)
                if len(k_list) < 5:
                    continue
                re_insert_x = """insert into {} ({}) values ({})""".format(key, k_keys, v_keys)
                print(re_insert_x)
                cursor.execute(re_insert_x)
                # cursor.execute('commit')
                # cursor.execute('select * from basic')
                # print(cursor.fetchall())
                # db.commit()

def extract_info_to_mysql(cursor, indir):
    cursor.execute('show databases')
    cursor.execute('use resume')
    for key in cmd_dict.keys():
        cursor.execute(cmd_dict[key])
    resumes = glob(os.path.join(indir, '*_json.txt'))
    for resume in resumes:
        extract_single_info_to_mysql(cursor, resume)
    cursor.execute('commit')
    db.commit()
    cursor.execute('select * from basic')
    print(cursor.fetchall())

resume_dir = '/Users/higgs/beast/code/work/ResumeAnalyze/try/resume_analyze_basicinfo/tzhuopin_output'
extract_info_to_mysql(cursor, resume_dir)