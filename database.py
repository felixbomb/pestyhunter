import sqlite3

def get_latest_tracks():
    conn = sqlite3.connect('pestyhunter.db')
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
    return tracks