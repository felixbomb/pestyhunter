import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geohash


def calc_distance(lat1, lon1):
    lat2=39.226876513413934
    lon2=-76.81521777415809
    R=6731
    lat1, lon1, lat2, lon2 =map(np.radians, [lat1, lon1, lat2, lon2])
    dlat=lat2-lat1
    dlon=lon2-lon1
    a = np.sin(dlat/2)**2 +np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c=2*np.arctan2(np.sqrt(a), np.sqrt(1-a))

    return R*c

def create_geohash(lat1, lon1):
    geohash_code = geohash.encode(lat1, lon1, precision=12)

conn = sqlite3.connect('pestyhunter.db')
#query="""SELECT t1.icao24, t1.latitude, t1.longitude, t1.timestamp, t1.priority, t1.altitude, t1.velocity
#FROM tracks t1
#JOIN (
#    SELECT icao24, MAX(timestamp) as max_timestamp
#    FROM tracks
#    GROUP BY icao24
#) t2 ON t1.icao24 = t2.icao24 AND t1.timestamp = t2.max_timestamp
#"""
query="SELECT icao24, latitude, longitude, priority, altitude, velocity FROM tracks"
df = pd.read_sql_query(query, conn)
#df['distance'] = df.apply(lambda row: calc_distance(row['latitude'], row['longitude']), axis=1)
#df['geohash'] = df.apply(lambda row: create_geohash(row['latitude'], row['longitude']), axis=1)
features = ['longitude', 'latitude','altitude', 'velocity'] 
X = df[features]
y = df['priority']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)


y_pred = rf_model.predict(X_test_scaled)


print(classification_report(y_test, y_pred))


feature_importance = pd.DataFrame({'feature': features, 'importance': rf_model.feature_importances_})
print(feature_importance.sort_values('importance', ascending=False))




n_samples = 5
sample_indices = np.random.choice(len(X_test), n_samples, replace=False)

for idx in sample_indices:
    sample = X_test_scaled[idx].reshape(1, -1)
    prediction = rf_model.predict(sample)[0]
    
    print(f"\nSample {idx}:")
    for feature, value in zip(features, X_test.iloc[idx]):
        print(f"{feature}: {value}")
    
    print(f"Predicted Priority: {prediction}")
    print("Feature Contributions:")
    
    
    feature_contribs = rf_model.feature_importances_ * sample[0]
    for feature, contrib in sorted(zip(features, feature_contribs), key=lambda x: abs(x[1]), reverse=True):
        print(f"{feature}: {contrib:.4f}")

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance.sort_values('importance', ascending=False))
plt.title('Feature Importance in Random Forest Model')
plt.tight_layout()
plt.show()

conn.close()