from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # YouTube video bağlantısını doğrula ve indir
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        file_path = stream.download(filename='video.mp4')

        return send_file(file_path, as_attachment=True, download_name='video.mp4')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
