from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import whisper
import time
from pydub import AudioSegment
from pydub.utils import which
import subprocess
import requests
import re
import azure.cognitiveservices.speech as speechsdk
import uuid

app = Flask(__name__)

# 启用跨域资源共享（CORS），允许前端与后端通信
from flask_cors import CORS
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin", "X-Custom-Header"])
  # 允许来自所有来源的请求

# 设置文件上传的目录和允许的文件类型
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
WHISPER_PATH = r'D:\work\VirtualDigitalPerson\Azure\.venv\Scripts\whisper.exe'
# 设置 whisper 路径（假设 Whisper 已经正确安装）
model = whisper.load_model("base")  # 加载 Whisper 模型

url = "http://127.0.0.1:8080/v1/completions"

# 检查文件扩展名是否允许上传
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_id():
    return str(uuid.uuid4())

def chat_with_llama(user_input):
    url = "http://127.0.0.1:8080/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "you are a helpful assistant"},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        completion = response.json().get("choices", [{}])[0].get("message", {}).get("content", "抱歉，返回的结果格式不正确。")
        return completion
    except requests.exceptions.RequestException as req_err:
        return "抱歉，无法生成回答。"

def text_to_speech(text: str, question_id: str):
    subscription_key = "EkCylr8dhwdgjbWfQBEVgi5ODYsxUQPFOlPILPx6s1MBaLGJTsfXJQQJ99ALAC3pKaRXJ3w3AAAYACOGBIC6"
    region = "eastasia"
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    audio_filename = f"output/response_{question_id}.wav"
    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return audio_filename
    else:
        return None

# 音频转文本功能
def convert_audio_to_text(audio_path):
    try:
        if not os.path.exists(audio_path):
            return None

        whisper_command = [WHISPER_PATH, audio_path, "--output_format", "txt", "--language", "zh"]
        result = subprocess.run(whisper_command, capture_output=True, text=True, encoding='utf-8')

        if result.returncode == 0:
            clean_transcription = result.stdout.strip()
            clean_transcription = re.sub(r"^Detected language:.*?$", "", clean_transcription, flags=re.MULTILINE)
            clean_transcription = re.sub(r"^Detecting.*?$", "", clean_transcription, flags=re.MULTILINE)
            clean_transcription = re.sub(r"\[.*?--.*?\]", "", clean_transcription)
            clean_transcription = clean_transcription.replace("\x1b[0m", "")

            if clean_transcription.strip():
                return clean_transcription.strip()
            else:
                return None
        else:
            return None

    except Exception as e:
        return None

# 上传接口，接收音频文件并保存至 uploads 目录
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'message': '没有文件部分'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        transcription = convert_audio_to_text(filepath)
        if transcription is None:
            return jsonify({'message': '音频转文本失败'}), 500

        AI_competition = chat_with_llama(transcription)

        question_id = generate_unique_id()
        audio_file_path = text_to_speech(AI_competition, question_id=question_id)

        if not audio_file_path:
            return jsonify({'message': '语音合成失败'}), 500

        return jsonify({
            'message': '文件上传成功',
            'filename': filename,
            'filepath': filepath,
            'transcription': transcription,
            'audio_file_path': audio_file_path
        }), 200
    else:
        return jsonify({'message': '不支持的文件格式'}), 400

@app.route('/output/<filename>')
def get_audio(filename):
    return send_from_directory('output', filename)

# 首页渲染，显示前端页面
@app.route('/')
def index():
    return render_template('index.html')

# 创建上传文件的目录（如果不存在）
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    # 绑定所有网络接口，允许外部设备访问
    app.run(host='0.0.0.0', port=3000, debug=True)
