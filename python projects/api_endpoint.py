from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/latest_tracks')
def get_latest_tracks():
    conn = sqlite3.connect('peskyhunter.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT icao24, callsign, longitude, latitude, altitude, velocity
        FROM tracks
        WHERE (icao24, timestamp) IN (
            SELECT icao24, MAX(timestamp)
            FROM tracks
            GROUP BY icao24
        )
    ''')
    
    tracks = [
        {
            "icao24": row[0],
            "callsign": row[1],
            "longitude": row[2],
            "latitude": row[3],
            "altitude": row[4],
            "velocity": row[5]
        }
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return jsonify(tracks)

if __name__ == '__main__':
    app.run(debug=True)