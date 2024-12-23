import azure.cognitiveservices.speech as speechsdk
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Azure Speech服务配置
subscription_key = "EkCylr8dhwdgjbWfQBEVgi5ODYsxUQPFOlPILPx6s1MBaLGJTsfXJQQJ99ALAC3pKaRXJ3w3AAAYACOGBIC6"
region = "eastasia"
speech_endpoint = "https://eastasia.api.cognitive.microsoft.com/"

# 读取音频文件
audio_filename = "D:\\studycode\\untitled\\input_wav\\output_audio.wav"  # 确保音频文件在当前工作目录下

# 配置音频输入
audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

# 配置语音识别
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

# 设置语言（可选，这里设置为中文简体）
speech_config.speech_recognition_language = "zh-CN"

# 创建语音识别器
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# 开始识别并获取结果
result = speech_recognizer.recognize_once()

# 处理识别结果
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(result.text)
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("没有语音被识别")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("语音识别被取消：", cancellation_details.reason)
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("错误详情：", cancellation_details.error_details)
