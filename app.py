import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


from water_frontend import util
from water_frontend import plots
from water_frontend import maps

def main():

    col1, col2 = st.columns([3,2])

    stations.sort_values('alt', ascending=False, inplace=True)

    # Station Selectbox (station_id selection)
    with col1 :

        station_id = st.selectbox('Station to Predict :',
                            stations.index,
                            format_func=lambda i: stations.loc[i, 'label'])

        label = stations.loc[station_id, 'label'].capitalize()
        river = stations.loc[station_id, 'river_label']
        alt = stations.loc[station_id, 'alt']
        lat = round(float(stations.loc[station_id, 'lat']),3)
        lon = round(float(stations.loc[station_id, 'lon']), 3)
        coord = f"({lat},{lon})"

        desc = f"""🌊 River : {river} | ⛰ Altitude : {alt}m |  Coordinates : {coord}"""
        st.write(desc)
        predict_asked = st.button('Predict')


    with col2 :
        st.pydeck_chart(maps.get_deck(stations, station_id))

    weather,prediction = util.get_predictions_dfs(station_id)

    if predict_asked :
        with col1 :
            pred_title = f"<h3 style='text-align: center;'>Water Quality Prediction at {label}</h3>"
            st.markdown(pred_title, unsafe_allow_html=True)
            st.pyplot(plots.prediction_figure(prediction))

        st.markdown("""---""")

        l,center,r = st.columns([1,3,1])

        with center :
            w_title = "<h2 style='text-align: center;'>"\
                "Weather Data Used by the Model</h2>"
            st.markdown(w_title, unsafe_allow_html=True)
            st.pyplot(plots.weather_figure(weather))

        with l :
            st.write(" ")
        with r :
            st.write(" ")


## MAIN CODE -------------------------------------------------------------------

st.set_page_config(
    page_title="Predict Water Pollution App",
    layout="wide",
)


title = "<h1 style='text-align: center;'>Water Quality Prediction</h1>"
st.markdown(title, unsafe_allow_html=True)


st.write("""A simple app predicting the Nitrate Concentration in the water
of the Saône River (France). The prediction is done using the Weather history and
forecast (precipitation, wind, temperature). The model used is a neural
network developped with TensorFlow. More info on
[Github](https://github.com/sebvey/water_prediction)""")

st.markdown("""---""")

stations = util.get_stations_df()

if stations is not None :
    main()

else :
    st.write('Prediction API currently Down... Sorry !')
