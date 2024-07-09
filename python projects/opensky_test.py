from opensky_api import OpenSkyApi
import sqlite3
api = OpenSkyApi()
states=api.get_states()
connection_obj= sqlite3.connect('pestyhunter.db')
cursor_obj=connection_obj.cursor()
table="""CREATE TABLE tracks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    icao24 TEXT NOT NULL,
    callsign TEXT,
    longitude REAL,
    latitude REAL,
    altitude REAL,
    velocity REAL,
    timestamp INTEGER NOT NULL
);"""
connection_obj.execute(table)
connection_obj.execute("CREATE INDEX idx_icao24_timestamp ON tracks(icao24, timestamp);")
connection_obj.commit()
connection_obj.close()

'''
class Track:
    def __init__(self, icao24, cs, lng, lat, alt, vel):
        self.icao24=icao24
        self.cs=cs
        self.lng=lng
        self.lat=lat
        self.alt=alt
        self.vel=vel
    def __repr__(self):
        return f"Track(icao24={self.icao24}, cs={self.cs}, lng={self.lng}, lat={self.lat}, alt={self.alt}, vel={self.alt}"

track_objects = []

for s in states.states:
    track=Track(
        s.icao24,
        s.callsign,
        s.longitude,
        s.latitude,
        s.baro_altitude,
        s.velocity,
    )
    track_objects.append(track)

'''
##to use when I eventually need to convert StateVectors into Track objects

