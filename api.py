import os
import subprocess
import requests
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow your PWA to talk to this API
CORS(app)

@app.route('/api/download')
def media_engine():
    source_url = request.args.get('url')
    file_type = request.args.get('type', 'video') 
    title = request.args.get('title', 'Void_Download').replace(" ", "_")

    if not source_url:
        return jsonify({"error": "No URL provided"}), 400

    # --- SUBTITLE DOWNLOAD ---
    if file_type == 'subtitle':
        try:
            r = requests.get(source_url, stream=True, timeout=10)
            ext = ".vtt" if ".vtt" in source_url.lower() else ".srt"
            return Response(
                r.iter_content(chunk_size=1024),
                mimetype='text/vtt',
                headers={"Content-Disposition": f"attachment; filename={title}{ext}"}
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # --- VIDEO DOWNLOAD (FFmpeg) ---
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
                "Content-Type": "video/mp4"
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Standard Flask start for local testing
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
