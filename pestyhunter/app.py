#Program: app.py
#Author: Felix Baum
#Last Updated: 8/20/24
#Description: Handles Flask web framework with up-to-date data from other programs
#Notes: Tracks are stored as a list of dictionaries containing icao24, lat/lon, velocity, acceleration, priority, and vertical rate values.
#Notes, continued: ai_class is added on with default value 0.


from flask import Flask, jsonify, send_from_directory, render_template_string, request
from database import get_latest_tracks
from pestyhunter import PestyHunter
import os
import logging

app = Flask(__name__)
Phunter=PestyHunter('pestyhunter.db')
Phunter.train_model()
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/latest_tracks')
def api_latest_tracks():
    #bbox set to the bounds of the PestyHunter ADS-B map
    min_lat = request.args.get('min_lat', type=float)
    max_lat = request.args.get('max_lat', type=float)
    min_lon = request.args.get('min_lon', type=float)
    max_lon = request.args.get('max_lon', type=float)

    bbox = None
    if all([min_lat, max_lat, min_lon, max_lon]):
        bbox = (min_lat, max_lat, min_lon, max_lon)
        app.logger.debug(f"Received bbox: {bbox}")

    tracks = get_latest_tracks(bbox)
    app.logger.debug(f"Returning {len(tracks)} tracks")
    predictions=Phunter.predict_latest()
    for track in tracks:
        track['ai_class'] = int(predictions.get(track['icao24'], 0))
    return jsonify({"tracks":tracks})

@app.route('/')
def index():
    if os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ADS-B Tracker</title>
        </head>
        <body>
            <h1>Pesky Hunter Map</h1>
            <p>Flask server fine, html file not in static folder, idiot.</p>
        </body>
        </html>
        """)

@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    node_modules_path = os.path.join(os.path.dirname(__file__), 'node_modules')
    return send_from_directory(node_modules_path, filename)

if __name__ == '__main__':
    app.run(port=5004, debug=True)
