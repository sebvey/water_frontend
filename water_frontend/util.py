import requests
from dotenv import dotenv_values
import pandas as pd

settings = dotenv_values()

def get_stations_df():
    """
    Requests the api for stations information
    Returns it as a DataFrame
    """

    url = settings['API_STATIONS_ENDPOINT']

    try:
        response = requests.get(url)

    except ConnectionError:
        return None

    if not response: # response not in 2XX
        return None

    return pd.DataFrame.from_dict(response.json(), orient='index')


def get_predictions_dfs(station_id):
    """
    Requests the api for 10 days prediction for the station
    Returns weather and prediction DataFrames
    """

    url = settings['API_PREDICTIONS_ENDPOINT']

    try:
        response = requests.get(url,params={'station_id':station_id})

    except ConnectionError:
        return None,None

    if not response: # response not in 2XX
        return None,None

    try :
        weather = pd.DataFrame.from_dict(response.json()['weather'], orient='index')
        prediction = pd.DataFrame.from_dict(response.json()['prediction'], orient='index')

        weather.index = pd.to_datetime(weather.index)
        prediction.index = pd.to_datetime(prediction.index)

        return (weather,prediction)
    except (ValueError, ConnectionError) :
        return None,None
