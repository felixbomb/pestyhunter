import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

class PestyHunterLite:
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
        train_data=df[df['timestamp']<most_recent_timestamp]
        #print("\nTraining DF Length: " + str(len(train_data.index)))

        # train_data = df.iloc[:-len(df['icao24'].unique())] 
        X = train_data[['latitude', 'longitude', 'velocity', 'vertical_rate','altitude']]
        y = train_data['priority']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        #print({self.model.score(X_test_scaled,y_test)})
        #features= ['latitude', 'longitude', 'velocity', 'vertical_rate', 'altitude']
        #feature_importance = pd.DataFrame({'feature': features, 'importance': self.model.feature_importances_})
        #print(feature_importance.sort_values('importance', ascending=False))

    def predict_latest(self):
        df=self.load_data()
        most_recent_timestamp = df['timestamp'].max()
        test_data=df[df['timestamp'] == most_recent_timestamp]
        #latest_data=df.iloc[df.groupby('icao24')['timestamp'].idxmax()]
        X_latest = test_data[['latitude', 'longitude', 'velocity', 'altitude', 'vertical_rate']]
        scaler = StandardScaler()
        X_latest_scaled = scaler.fit_transform(X_latest)
        predictions=self.model.predict(X_latest_scaled)
        prediction_dict = dict(zip(test_data['icao24'], predictions))
        return prediction_dict
    
Phunter=PestyHunterLite('pestyhunter.db')
Phunter.train_model()
latest_predictions = Phunter.predict_latest()


#print(latest_predictions)