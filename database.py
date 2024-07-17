import sqlite3

    
def get_latest_tracks(bbox=None):
    conn = sqlite3.connect('pestyhunter.db')  
    cursor = conn.cursor()

    if bbox:
        min_lat, max_lat, min_lon, max_lon = bbox
        query = """
        SELECT t1.*
        FROM tracks t1
        JOIN (
            SELECT icao24, MAX(timestamp) as max_timestamp
            FROM tracks
            WHERE latitude BETWEEN ? AND ?
            AND longitude BETWEEN ? AND ?
            GROUP BY icao24
        ) t2 ON t1.icao24 = t2.icao24 AND t1.timestamp = t2.max_timestamp
        """
        cursor.execute(query, (min_lat, max_lat, min_lon, max_lon))
        #selects newest iteration of each icao24 listing
        print("tracks found within bbox")
    else:
        query = """
        SELECT t1.*
        FROM tracks t1
        JOIN (
            SELECT icao24, MAX(timestamp) as max_timestamp
            FROM tracks
            GROUP BY icao24
        ) t2 ON t1.icao24 = t2.icao24 AND t1.timestamp = t2.max_timestamp
        """
        cursor.execute(query)
        print("tracks found")
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()

    return results