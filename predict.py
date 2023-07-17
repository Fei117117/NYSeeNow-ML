from flask import Flask, request, jsonify
import pickle
import numpy as np
import os
import pandas as pd
from haversine import haversine

app = Flask(__name__)

models = {}

# Load station data
stations_df = pd.read_csv(
    '/SubwayData/cleaned_station_data.csv')


def get_nearest_station_id(lon, lat):
    # Calculate the distance from the provided coordinates to all stations
    distances = stations_df.apply(lambda row: haversine(
        (lon, lat), (row['lon'], row['lat'])), axis=1)

    # Get the id of the nearest station
    nearest_station_id = stations_df.loc[distances.idxmin(), 'remote_unit_id']

    return nearest_station_id


@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    # Extract relevant information from the data structure
    lon = data['geometry']['coordinates'][0]
    lat = data['geometry']['coordinates'][1]
    day = pd.to_datetime(data['day']).weekday() + 1
    month = pd.to_datetime(data['day']).month

    # Get the nearest station id
    station_number = get_nearest_station_id(lon, lat)
    type = 'station'  # area or station

    if type == 'area':
        path = f'/SubwayData/{type}_busy/a_busy_model_{station_number}.pkl'
    elif type == 'station':
        path = f'/SubwayData/{type}_busy/s_busy_model_{station_number}.pkl'
    else:
        return jsonify({'error': 'Invalid type.'})

    try:
        # Load the model
        with open(path, 'rb') as handle:
            model = pickle.load(handle)
    except FileNotFoundError:
        return jsonify({'error': 'Model not found.'})

     # Prepare the response structure
    response = {}

    # Iterate over all 24 hours
    for hour in range(24):
        # Prepare the input for the model including hour, day, month, and other required parameters
        model_input = pd.DataFrame({
            'hour': [hour],
            'day': [day],
            'month': [month],
            'temperature': [15.3],  # Replace with actual temperature value
            'rain_fall': [2.6],  # Replace with actual rain_fall value
            'snow_fall': [0.0],  # Replace with actual snow_fall value
            'Clear': [0],
            'Clouds': [0],
            'Drizzle': [0],
            'Fog': [0],
            'Haze': [0],
            'Mist': [0],
            'Rain': [1],
            'Smoke': [0],
            'Snow': [0],
            'Thunderstorm': [0]
        })

        # Make prediction using the loaded model and the input data
        prediction = model.predict(model_input.values)

        # Take the first value of the prediction
        output = prediction[0]

        # Add the busyness for the current hour to the response
        response[str(hour)] = int(output)

    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
