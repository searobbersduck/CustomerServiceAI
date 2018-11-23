# !/usr/bin/env python3

import wave
import pyaudio
from pyaudio import PyAudio, paInt16
from aip import AipSpeech

CUID = '93489083242'
DEV_PID = 1537

# 用Pyaudio库录制音频
#   out_file:输出音频文件名
#   rec_time:音频录制时间(秒)
def audio_record(out_file, rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")
    # 保存音频文件
    wf = wave.open(out_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def get_file_content(file):
    audio_file = file
    f = open(audio_file, 'rb+')
    sound_wav_rb = f.read()
    f.close()
    return sound_wav_rb

# 读取paudio录制好的音频文件, 调用百度语音API, 设置api参数, 完成语音识别
#    client:AipSpeech对象
#    afile:音频文件
#    afmt:音频文件格式(wav)
def aip_get_asrresult(client, afile, afmt):
    # 选项参数:
    # cuid    String  用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
    # dev_pid String  语言类型(见下表), 默认1537(普通话 输入法模型)
    # 识别结果已经被SDK由JSON字符串转为dict
    result = client.asr(get_file_content(afile), afmt, 16000, {"cuid": CUID, "dev_pid": DEV_PID,})
    #print(result)
    # 如果err_msg字段为"success."表示识别成功, 直接从result字段中提取识别结果, 否则表示识别失败
    if result["err_msg"] == "success.":
        #print(result["result"])
        return result["result"]
    else:
        #print(result["err_msg"])
        return ""


import io

def audio_record_rt(rec_time):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #16bit编码格式
    CHANNELS = 1 #单声道
    RATE = 16000 #16000采样频率
    p = pyaudio.PyAudio()
    # 创建音频流
    stream = p.open(format=FORMAT, # 音频流wav格式
                    channels=CHANNELS, # 单声道
                    rate=RATE, # 采样率16000
                    input=True,
                    frames_per_buffer=CHUNK)
    print("Start Recording...")
    frames = [] # 录制的音频流
    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * rec_time)):
        data = stream.read(CHUNK)
        frames.append(data)
    # 录制完成
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Done...")
    # 保存音频文件
    with io.BytesIO() as wav_file:
        wf = wave.open(wav_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        wav_data = wav_file.getvalue()
    return wav_data

def audio_interact():
    client = AipSpeech('14922410', 'NSChZHWWVwa1BSwZ36Oaya4C', '1dd0sxs2LXYRWETZ4gZSSDYDQvM6aROv')
    while True:
        result = client.asr(audio_record_rt(5), 'wav', 16000, {"cuid": CUID, "dev_pid": DEV_PID, })
        if result["err_msg"] == "success.":
            # print(result["result"])
            print(result["result"])
        else:
            # print(result["err_msg"])
            # return ""
            pass

if __name__ == '__main__':
    # audio_record('demo.wav', 5)
    # client = AipSpeech('14922410','NSChZHWWVwa1BSwZ36Oaya4C','1dd0sxs2LXYRWETZ4gZSSDYDQvM6aROv')
    # aip_get_asrresult(client, 'demo.wav', 'wav')
    audio_interact()