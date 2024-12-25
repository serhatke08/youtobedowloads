from flask import Flask, request, send_file, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        # YouTube video URL'sinden video dosyasını indirme işlemi
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            file_path = 'video.mp4'
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return send_file(file_path, as_attachment=True, download_name='video.mp4')
        else:
            return jsonify({'error': 'Failed to download video. Please check the URL.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)