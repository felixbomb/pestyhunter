from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
conn=sqlite3.connect('peskyhunter.db')
cursor=conn.cursor()
cursor.execute("ALTER TABLE tracks ADD COLUMN priority INTEGER DEFAULT 0")

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
    
   