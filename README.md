# PestyHunter

PestyHunterAI is an open-source proof-of-concept project created by Felix Baum at Focused Support, LLC.

This GitHub repository is part of a larger document entitled "Tactical Situation Displays in the Era of Artificial Intelligence"

PestyHunter operates using a RandomForestClassifier library from scikit-learn, live flight data from OpenSky's API, and Leaflet's handy HTML/CSS map.

No updates/bugfixes have been made to this project since August 20, 2024.
This project and its associated documentation are shared under the [MIT](https://choosealicense.com/licenses/mit/#) license. 

## Installation
In lieu of a dedicated release or package, all of the code involved in PestyHunter is available as-is in this repository, where the good people of the world may fork it as they see fit.
The required packages/libraries are listed below and in requirements.txt. Installation of OpenSkyAPI is also required, which can be accessed [here.](https://openskynetwork.github.io/opensky-api/)

## Dependencies
Flask==3.0.3

pandas==2.2.2

Requests==2.32.3

scikit_learn==1.5.1

setuptools==73.0.0

sphinx_rtd_theme==2.0.0

leaflet=1.94
	
leaflet-rotatedmarker==0.2.0

## Database
The PestyHunter database, pestyhunter.db is an SQLite 3 database with over 200,000 columns of timestamped ADS-B data from the OpenSkyAI.

PestyHunterAI seeks to reverse engineer the automatic priority logic contained in updater.py. This logic is customizable, but only data pulled in after a logic modification should be used when training PestyHunterAI to prevent contaminating the training data and weakening the model's performance.

## Usage
After installing all necessary dependencies and importing the project files, PestyHunter is yours to experiment with.
In a Python terminal, begin by calling updater.py

```python
cd pestyhunter
python3 updater.py
```
This will automatically draw in new data from the OpenSkyAPI every 5 seconds, depositing it in pestyhunter.db
In another Python terminal, call app.py
```python
cd pestyhunter
python3 app.py
```
This sets up the Flask app routing to allow you to display your ADS-B data and PestyHunter's predictions.