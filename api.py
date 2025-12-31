import os
import subprocess
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def health():
    return "Void API: Online", 200

@app.route('/api/download')
def download():
    url = request.args.get('url')
    title = request.args.get('title', 'Void_Media').replace(" ", "_")

    if not url:
        return "No URL provided", 400

    # These headers are the 'Secret Sauce' to bypass blocks
    # We pretend the request is coming from the video player itself
    headers = (
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
        "Referer: https://vidsrc.me/\r\n"
        "Origin: https://vidsrc.me\r\n"
    )

    ffmpeg_cmd = [
        'ffmpeg',
        '-headers', headers,
        '-i', url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        '-f', 'mp4',
        '-movflags', 'frag_keyframe+empty_moov+faststart',
        'pipe:1'
    ]

    try:
        # We capture stderr to see exactly WHY it fails in the Render logs
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
