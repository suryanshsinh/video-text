from flask import Flask, request, jsonify
from moviepy.editor import *
import whisper
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/video-text', methods=['POST'])
def video_text():
    data = request.json
    video_name = data['video'].split("/")[-1].split(".")[0]
    video = VideoFileClip(data['video'])
    video.audio.write_audiofile(f"./{video_name}.mp3")
    model = whisper.load_model("base")
    result = model.transcribe(f"./{video_name}.mp3")
    return result['text']

if __name__ == '__main__':
    app.run()
