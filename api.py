import os
import subprocess
import requests
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/download')
def media_engine():
    source_url = request.args.get('url')
    file_type = request.args.get('type', 'video') 
    title = request.args.get('title', 'Void_Download').replace(" ", "_")

    if not source_url:
        return jsonify({"error": "No URL"}), 400

    if file_type == 'subtitle':
        r = requests.get(source_url, stream=True)
        return Response(r.iter_content(1024), mimetype='text/vtt')

    # FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-headers', 'Referer: https://vidsrc.me/\r\n',
        '-i', source_url,
        '-c', 'copy', 
        '-bsf:a', 'aac_adtstoasc',
        '-f', 'mp4',
        '-movflags', 'frag_keyframe+empty_moov+faststart',
        'pipe:1'
    ]

    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE)
    return Response(process.stdout, mimetype='video/mp4', 
                    headers={"Content-Disposition": f"attachment; filename={title}.mp4"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))