import azure.cognitiveservices.speech as speechsdk
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# Azure Speech服务配置
subscription_key = "EkCylr8dhwdgjbWfQBEVgi5ODYsxUQPFOlPILPx6s1MBaLGJTsfXJQQJ99ALAC3pKaRXJ3w3AAAYACOGBIC6"
region = "eastasia"
speech_endpoint = "https://eastasia.api.cognitive.microsoft.com/"

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 构造音频文件的绝对路径
audio_filename = os.path.join(script_dir, "uploads", "audio.wav")

# 打印音频文件路径（调试用）
print(f"音频文件路径：{audio_filename}")

# 检查文件是否存在
if not os.path.exists(audio_filename):
    print(f"错误：音频文件不存在！路径：{audio_filename}")
    sys.exit(1)

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
