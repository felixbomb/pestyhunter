import sqlite3

def get_latest_tracks(bbox=None):
    conn = sqlite3.connect('pestyhunter.db')
    cursor = conn.cursor()
    
    query='''
        SELECT t1.icao24, t1.callsign, t1.longitude, t1.latitude, t1.altitude, t1.velocity
        FROM tracks t1
        INNER JOIN(
            SELECT icao24, MAX(timestamp) as max_timestamp
            FROM tracks
            GROUP BY icao24
            ) t2 ON t1.icao24 AND t1.timestamp = t2.max_timestamp
    '''
    params=[]
    if bbox:
        query += ' AND latitude BETWEEN ? AND ? and longitude BETWEEN ? and ?'
        params = [bbox[0], bbox[1], bbox[2], bbox[3]]
    cursor.execute(query, params)
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