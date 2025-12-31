import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Void API is Live! Use /api/download for media."

@app.route('/api/download')
def download():
    url = request.args.get('url')
    if not url:
        return "Missing URL", 400
    
    # Simple FFmpeg command for testing
    ffmpeg_cmd = [
        'ffmpeg', '-headers', 'User-Agent: Mozilla/5.0\r\n',
        '-i', url, '-c', 'copy', '-f', 'mp4', 
        '-movflags', 'frag_keyframe+empty_moov+faststart', 'pipe:1'
    ]
    
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    return Response(process.stdout, mimetype='video/mp4')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
