import os
import subprocess
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Test Route: If you visit the main URL, you should see this message.
@app.route('/')
def index():
    return "Void API is Running. Use /api/download for media."

@app.route('/api/download')
def download():
    source_url = request.args.get('url')
    file_type = request.args.get('type', 'video')
    title = request.args.get('title', 'Media').replace(" ", "_")

    if not source_url:
        return "Missing URL parameter", 400

    # FFmpeg Command
    ffmpeg_cmd = [
        'ffmpeg',
        '-headers', 'Referer: https://vidsrc.me/\r\nUser-Agent: Mozilla/5.0\r\n',
        '-i', source_url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        '-f', 'mp4',
        '-movflags', 'frag_keyframe+empty_moov+faststart',
        'pipe:1'
    ]

    try:
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return Response(
            process.stdout,
            mimetype='video/mp4',
            headers={"Content-Disposition": f"attachment; filename={title}.mp4"}
        )
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
