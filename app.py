from cProfile import label
from sqlalchemy import lateral
import streamlit as st
import pandas as pd

import os
from dotenv import dotenv_values


from water_frontend import util
from water_frontend import plots
from water_frontend import maps

settings = dotenv_values()
os.environ['MAPBOX_API_KEY'] = settings['MAPBOX_API_KEY']

def main():

    title = "<h1 style='text-align: center;'>Water Quality Prediction</h1>"
    st.markdown(title, unsafe_allow_html=True)

    st.write("""A simple app predicting the Nitrate Concentration in the water
    of the Saône River (France). The prediction is done using the Weather history and
    forecast (precipitation, wind, temperature). The model used is a neural
    network developped with TensorFlow. More details HERE.""")

    col1, col2 = st.columns([1,1])

    stations.sort_values('alt', ascending=False, inplace=True)

    # Station Selectbox (station_id selection)
    with col1 :
        station_id = st.selectbox('Station to Predict :',
                              stations.index,
                              format_func=lambda i: stations.loc[i, 'label'])

    label = stations.loc[station_id, 'label'].capitalize()
    river = stations.loc[station_id, 'river_label']
    alt = stations.loc[station_id, 'alt']
    lat = round(float(stations.loc[station_id, 'lat']),2)
    lon = round(float(stations.loc[station_id, 'lon']), 2)
    coord = f"({lat},{lon})"

    desc = f"""🌊 River : {river}
            ⛰ Altitude : {alt}m
            📍 GPS Coordinates : {coord}"""

    with col1 :
        for line in desc.splitlines() :
            st.write(line)

    with col2 :
        st.pydeck_chart(maps.get_deck(stations, station_id))

    weather,prediction = util.get_predictions_dfs(station_id)

    pred_title = f"<h3 style='text-align: center;'>Water Quality Prediction at {label}</h3>"
    st.markdown(pred_title, unsafe_allow_html=True)
    st.pyplot(plots.prediction_figure(prediction))


    w_title = "<h2 style='text-align: center;'>"\
        "Weather Data Used by the Model</h2>"
    st.markdown(w_title, unsafe_allow_html=True)
    st.pyplot(plots.weather_figure(weather))







stations = util.get_stations_df()

if stations is not None :
    main()

else :
    st.write('Prediction API currently Down... Sorry !')
