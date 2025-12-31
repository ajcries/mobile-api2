import os
import subprocess
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)

# This configuration allows all origins, all methods (GET, POST, etc.), 
# and all headers. It's the most permissive setting possible.
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def health_check():
    return "Void API: Online and CORS-Open", 200

@app.route('/api/download')
def download():
    source_url = request.args.get('url')
    file_type = request.args.get('type', 'video')
    title = request.args.get('title', 'Media_File').replace(" ", "_")

    if not source_url:
        return "Error: No URL provided", 400

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
            headers={
                "Content-Disposition": f"attachment; filename={title}.mp4",
                "Access-Control-Allow-Origin": "*" # Extra security layer for direct file access
            }
        )
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
