# 杀掉已存在服务
ps -ef | grep bert-serving- | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep qs_matching_server | grep -v grep | awk '{print $2}' | xargs kill
# 启动服务
source deactivate
source activate py36
bert-serving-start -model_dir ./model/chinese_L-12_H-768_A-12/ -max_seq_len 50&
echo 'start question matching server ...'
sleep 30
# 启动语义匹配服务
python qs_matching_server.py &