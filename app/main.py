from flask import Blueprint, request, jsonify
from moviepy.editor import *
import whisper
from .celery_config import make_celery
from . import create_app

bp = Blueprint('main', __name__)
app = create_app()  # Initialize the Flask app
celery = make_celery(app)

@bp.route('/')
def hello_world():
    return 'Hello, World!'

@bp.route('/video-text', methods=['POST'])
def video_text():
    data = request.json
    task = process_video.delay(data['video'])
    return jsonify({'task_id': task.id})

@bp.route('/status/<task_id>')
def taskstatus(task_id):
    task = process_video.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),
        }
    return jsonify(response)

@celery.task(bind=True)
def process_video(self, video_path):
    video_name = video_path.split("/")[-1].split(".")[0]
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(f"./{video_name}.mp3")
    model = whisper.load_model("base")
    result = model.transcribe(f"./{video_name}.mp3")
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': result['text']}
