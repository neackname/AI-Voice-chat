import azure.cognitiveservices.speech as speechsdk
import sys
def text_to_speech(text:str):

    # 固定音色、语调、语气、情绪等配置
    voice_name = "zh-CN-XiaoxiaoNeural"  # 女声
    prosody = "medium"  # 正常语调
    style = "neutral"  # 正常语气
    emotion = "happy"  # 开心情绪

    # 配置Azure Speech服务
    subscription_key = "EkCylr8dhwdgjbWfQBEVgi5ODYsxUQPFOlPILPx6s1MBaLGJTsfXJQQJ99ALAC3pKaRXJ3w3AAAYACOGBIC6"
    region = "eastasia"
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # 设置语音参数
    speech_config.speech_synthesis_voice_name = voice_name

    # 配置音频输出到文件
    audio_config = speechsdk.audio.AudioConfig(filename="D:\\studycode\\untitled\\output_wav\\output_audio.wav")

    # 创建TTS语音合成器
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # 合成语音并检查结果
    result = synthesizer.speak_text_async(text).get()

    # 检查合成是否成功
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("音频已合成，输出文件为 output_audio.wav")
    else:
        print("语音合成失败: ", result.error_details)

if __name__ == "__main__":
    if len(sys.argv) >1:
        text = sys.argv[1]
        text_to_speech(text)
    else:
        print("未提供文本参数")