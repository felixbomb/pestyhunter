import sqlite3
import time
from opensky_api import OpenSkyApi
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c
    return distance
def calculate_priority(distance, altitude, vertical_rate, velocity):
    priority=0
    if (distance < 8 and velocity > 100 and altitude != None):
        if (altitude < 5000 and vertical_rate <0.000):
            priority=3
        elif(altitude<5000):
            priority=2
        elif(altitude <10000):
            priority=1
    elif (distance < 16 and altitude!=None):
        if (altitude < 5000):
            priority=1
        elif(altitude <10000):
            priority=0
    elif(distance < 32 and altitude!=None):
        if(vertical_rate >0.000 and altitude > 10000):
            priority=1
    return priority

def update_tracks(db_path, bbox=None):
    api = OpenSkyApi("felixbaum", "S0ylentOpenSky!")
#i should probably hide my login details when publishing to my github, but i'll figure that out later
#attempted to add heading support 3:09PM 7/24/24
#succeeded 12:09PM 7/25/24
    while True:
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            #sets up connection and cursor for SQLite
            states = api.get_states(bbox=bbox) if bbox else api.get_states()
            current_time = int(time.time())
            #sets up timestamp and gets statevectors from OpenSky within the bounding box range
            if states is not None and states.states:
                #weird error handling, if my refresh rate for the updater is too high then OpenSky returns None for states
                for s in states.states:
                    distance=calculate_distance(39.226876513413934, -76.81521777415809, s.latitude, s.longitude)
                    priority=calculate_priority(distance, s.baro_altitude, s.vertical_rate, s.velocity)
                    cursor.execute('''
                        INSERT INTO tracks (icao24, callsign, longitude, latitude, altitude, velocity, timestamp, priority, heading, vertical_rate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (s.icao24, s.callsign, s.longitude, s.latitude, s.baro_altitude, s.velocity, current_time, priority, s.true_track, s.vertical_rate))
                    #keeping old tracks w timestamp data so PeskyHunter AI can access historical data later
                conn.commit()
                print(f"Updated {len(states.states)} tracks at {current_time}")
                #normal operation in default bbox updates about 90-150 tracks every 5 secs
            else:
                print(f"No data received from API at {current_time}")

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
        #except Exception as e:
        #    print(f"Oops! An unexpected error occurred: {e}")
        finally:
            if conn:
                conn.close()

        time.sleep(5)
        #the magic number. anything lower breaks the code, anything higher is annoyingly slow

if __name__ == "__main__":
    default_bbox = (38.7465862524827, 39.70401708565211, -77.97821044921876, -75.65185546875001)
    update_tracks('pestyhunter.db', bbox=default_bbox)