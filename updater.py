import sqlite3
import time
from opensky_api import OpenSkyApi

def update_tracks(db_path):
    api = OpenSkyApi()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        try:
            states = api.get_states()
            current_time = int(time.time())

            if states is not None and states.states is not None:
                for s in states.states:
                    cursor.execute('''
                        INSERT INTO tracks (icao24, callsign, longitude, latitude, altitude, velocity, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (s.icao24, s.callsign, s.longitude, s.latitude, s.baro_altitude, s.velocity, current_time))

                conn.commit()
                print(f"Updated {len(states.states)} tracks at {current_time}")
            else:
                print(f"No data received from API at {current_time}")

        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(10)

    conn.close()

if __name__ == "__main__":
    update_tracks('pestyhunter.db')