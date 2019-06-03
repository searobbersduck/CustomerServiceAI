import os
import wave
import numpy as np
import pyaudio
import fire

file1 = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '音频文件/执迷不悟.wav')

# f = wave.open(file1, "rb")
#
# params = f.getparams()
# nchannels, sampwidth, framerate, nframes = params[:4]
# print(nchannels, sampwidth, framerate, nframes)  # 2 2 44100 11625348
# # 读取波形数据
# str_data = f.readframes(nframes)
# f.close()
#
# # 将波形数据转换为数组
# wave_data = np.fromstring(str_data, dtype=np.int16)
# wave_data.shape = -1, 2
# wave_data = wave_data.T
#
# wave_data_1 = wave_data[0]  # 声道1
# wave_data_2 = wave_data[1]  # 声道2
#
# w1 = wave_data_1.tostring()
# w2 = wave_data_2.tostring()
#
# # 实现录音
# def record(re_frames, WAVE_OUTPUT_FILENAME):
#     """
#     :param re_frames: 是二进制的数据
#     :param WAVE_OUTPUT_FILENAME: 输出的位置
#     :return:
#     """
#     p = pyaudio.PyAudio()
#     CHANNELS = 1
#     FORMAT = pyaudio.paInt16
#     RATE = framerate  # 这个要跟原音频文件的比特率相同
#     print("开始录音")
#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(re_frames)
#     wf.close()
#     print("关闭录音")
#
# record(w1, os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '音频文件/执迷不悟1.wav'))
# record(w1, os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '音频文件/执迷不悟2.wav'))

def convert2_to_1(infile, outdir):
    f = wave.open(infile, "rb")

    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print(nchannels, sampwidth, framerate, nframes)  # 2 2 44100 11625348
    # 读取波形数据
    str_data = f.readframes(nframes)
    f.close()

    # 将波形数据转换为数组
    wave_data = np.fromstring(str_data, dtype=np.int16)
    wave_data.shape = -1, 2
    wave_data = wave_data.T

    wave_data_1 = wave_data[0]  # 声道1
    wave_data_2 = wave_data[1]  # 声道2

    w1 = wave_data_1.tostring()
    w2 = wave_data_2.tostring()

    # 实现录音
    def record(re_frames, WAVE_OUTPUT_FILENAME):
        """
        :param re_frames: 是二进制的数据
        :param WAVE_OUTPUT_FILENAME: 输出的位置
        :return:
        """
        p = pyaudio.PyAudio()
        CHANNELS = 1
        FORMAT = pyaudio.paInt16
        RATE = framerate  # 这个要跟原音频文件的比特率相同
        print("开始录音")
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(re_frames)
        wf.close()
        print("关闭录音")
    basename = os.path.basename(infile).split('.')[0]
    record(w1, os.path.join(outdir, basename+'_1.wav'))
    record(w2, os.path.join(outdir, basename+'_2.wav'))

if __name__ == '__main__':
    fire.Fire()