from flask import Flask, jsonify, send_from_directory
from database import get_latest_tracks

app = Flask(__name__)

@app.route('/api/latest_tracks')
def api_latest_tracks():
    tracks = get_latest_tracks()
    return jsonify(tracks)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)