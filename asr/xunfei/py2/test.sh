# usage: ./test.sh ~/beast/data/audio/兔司机与候选人首次沟通录音
ls *.wav

if [ ! -d ~/tmpxxx ]
then
	echo 'directory not exists'
	mkdir -p ~/tmpxxx
fi

if [ ! -d ~/tmpxxx_c1_all ]
then
	echo 'directory not exists'
	mkdir -p ~/tmpxxx_c1_all
fi

if [ ! -d ~/tmpxxx_c1_single ]
then
	echo 'directory not exists'
	mkdir -p ~/tmpxxx_c1_single
fi

if [ ! -d ~/tmpxxx_txt ]
then
	echo 'directory not exists'
	mkdir -p ~/tmpxxx_txt
fi

echo $1

if [ -d $1 ]
then
	for file in $1/*.wav;do
		echo $(basename $file)
		ffmpeg -y  -i $file -acodec pcm_s16le -f s16le -ac 2 -ar 16000 ~/tmpxxx_c1_all/$(basename $file)
		# 先利用ffmpeg将压缩的wav文件转换为，python能够读取的非压缩形式，采样率设置为16000，便于语音识别使用
		ffmpeg -i $file -acodec pcm_s16le -ar 16000 -y ~/tmpxxx/$(basename $file)
	done
fi

source deactivate
source activate py36
for file in ~/tmpxxx/*.wav;do
    python convert_channel2_to_1.py convert2_to_1 $file ~/tmpxxx_c1_single
done
source deactivate
source activate py27
for file in ~/tmpxxx_c1_single/*.wav;do
    python parse_audio_rt.py paser_audio_rt $file ~/tmpxxx_txt
done
for file in ~/tmpxxx_c1_all/*.wav;do
    python parse_audio_rt.py paser_audio_rt $file ~/tmpxxx_txt
done
source deactivate

rm -rf ~/tmpxxx
rm -rf ~/tmpxxx_c1_all
rm -rf ~/tmpxxx_c1_single
#rm -rf ~/tmpxxx_txt