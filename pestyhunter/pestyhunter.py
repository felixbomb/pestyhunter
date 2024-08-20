#Program: PestyHunter.py
#Author: Felix Baum
#Last Updated: 8/20/24
#Description: Uses scikit-learn Random Classifier to reverse-engineer priority classification logic established in updater.py
#Notes: PestyHunter model is trained on old data, and sent newest data from app.py for live testing.

import pandas as pd
import sqlite3
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder

class PestyHunter:
    def __init__(self, db_path):
        self.db_path = db_path
        self.model = None
        self.le=LabelEncoder()

    def load_data(self):
        conn = sqlite3.connect('pestyhunter.db')
        query="SELECT icao24, latitude, longitude, priority, altitude, velocity, vertical_rate, timestamp FROM tracks"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def train_model(self):
        df=self.load_data()
        most_recent_timestamp = df['timestamp'].max()
        #train_data is selected from all icao24 listings that are not associated with the most recent timestamp
        train_data=df[df['timestamp']<most_recent_timestamp]
        #PestyHunter is fed lat/lon, velocity, vertical_rate, and altitude as these are the factors used in automatic priority classing in updater.py
        X_train = train_data[['latitude', 'longitude', 'velocity', 'vertical_rate','altitude']]
        y_train = train_data['priority']
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)

    def predict_latest(self):
        df=self.load_data()
        most_recent_timestamp = df['timestamp'].max()
        #test_data is selected from all icao24 listings that are associated with the most recent timestamp
        test_data=df[df['timestamp'] == most_recent_timestamp]
        X_test = test_data[['latitude', 'longitude', 'velocity', 'altitude', 'vertical_rate']]
        scaler = StandardScaler()
        X_test_scaled = scaler.fit_transform(X_test)
        predictions=self.model.predict(X_test_scaled)
        prediction_dict = dict(zip(test_data['icao24'], predictions))
        return prediction_dict
    
Phunter=PestyHunter('pestyhunter.db')
Phunter.train_model()
latest_predictions = Phunter.predict_latest()


