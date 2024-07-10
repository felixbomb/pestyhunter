import sqlite3
import time
from opensky_api import OpenSkyApi

def update_tracks(db_path, bbox=None):
    api = OpenSkyApi("felixbaum", "S0ylentOpenSky!")
#i should probably hide my login details when publishing to my github, but i'll figure that out later
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
                    cursor.execute('''
                        INSERT INTO tracks (icao24, callsign, longitude, latitude, altitude, velocity, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (s.icao24, s.callsign, s.longitude, s.latitude, s.baro_altitude, s.velocity, s.time_position or current_time))
                    #keeping old tracks w timestamp data so PeskyHunter AI can access historical data later
                conn.commit()
                print(f"Updated {len(states.states)} tracks at {current_time}")
                #normal operation in default bbox updates about 90-150 tracks every 5 secs
            else:
                print(f"No data received from API at {current_time}")

        except sqlite3.Error as e:
            print(f"A database error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if conn:
                conn.close()

        time.sleep(5)
        #the magic number. anything lower breaks the code, anything higher is annoyingly slow

if __name__ == "__main__":
    default_bbox = (45.8389, 47.8229, 5.9962, 10.5226)
    update_tracks('pestyhunter.db', bbox=default_bbox)