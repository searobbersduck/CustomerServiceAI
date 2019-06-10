# usage: ./test.sh ~/beast/data/audio/兔司机与候选人首次沟通录音 1

export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'

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

echo $1

if [ -d $1 ]
then
	for file in $1/*.wav;do
		echo $(basename $file)
        ffmpeg -y  -i $file -acodec pcm_s16le -f s16le -ar 16000 ~/tmpxxx_c1_all/$(basename $file)
	done
fi

source deactivate
source activate py36
#for file in ~/tmpxxx/*.wav;do
#    python convert_channel2_to_1.py convert2_to_1 $file ~/tmpxxx_c1_single
#done
source deactivate
source activate py27
outdir="./tmpxxx_"$2"_txt"
for file in ~/tmpxxx_c1_all/*.wav;do
    python parse_audio_rt.py paser_audio_rt $file $outdir
done
source deactivate

rm -rf ~/tmpxxx
rm -rf ~/tmpxxx_c1_all
#rm -rf ./tmpxxx_$2_txt