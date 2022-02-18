import pydeck as pdk
import pandas as pd

from water_frontend import util

import os


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(MODULE_DIR,'..','data')
DATA_DIR = os.path.normpath(DATA_DIR)
SAONE_TRACE_PICKLE_PATH = os.path.join(DATA_DIR, 'saone_trace.pickle')
saone_trace = pd.read_pickle(SAONE_TRACE_PICKLE_PATH)


def get_deck(stations,station_id):

    # Sets the icons data
    # Current station is red, others are green

    # GREEN_ICON_URL = os.path.join(DATA_DIR,'location_icon_green.png')
    # RED_ICON_URL = os.path.join(DATA_DIR,'location_icon_red.png')

    GREEN_ICON_URL = 'https://raw.githubusercontent.com/sebvey/water_frontend/main/data/location_icon_green.png'
    RED_ICON_URL = 'https://raw.githubusercontent.com/sebvey/water_frontend/main/data/location_icon_red.png'



    green_icon_data = {
        "url": GREEN_ICON_URL, # util.get_png_data_url(GREEN_ICON_URL),
        "width": 128,
        "height": 128,
        "anchorY": 128,
    }

    red_icon_data = {
        "url": RED_ICON_URL, # util.get_png_data_url(RED_ICON_URL),
        "width": 128,
        "height": 128,
        "anchorY": 128,
    }

    stations["icon_data"] = None
    stations["icon_size_scale"] = None

    for i in stations.index :
        stations.loc[i,'icon_data'] = [green_icon_data]
        stations.loc[i, 'icon_size'] = 7

    stations.loc[station_id,'icon_data'] = [red_icon_data]
    stations.loc[station_id, 'icon_size'] = 9

    # View coordiantes = actual station coordinates
    lat = stations.loc[station_id,'lat']
    lon = stations.loc[station_id,'lon']

    # pydeck code
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=9,
        min_zoom=5,
        max_zoom=13,
        pitch=0,
    )

    saone_layer = pdk.Layer(
        type="PathLayer",
        data=saone_trace,
        get_color="color",
        width_scale=40,
        width_min_pixels=5,
        opacity=0.7,
        joint_rounded=True,
        cap_rounded=True,
        get_path="path",
        get_width=5,
    )

    icon_layer = pdk.Layer(
        type="IconLayer",
        data=stations,
        get_icon="icon_data",
        get_size="icon_size",
        size_scale=5,
        get_position=["lon", "lat"],
    )

    deck = pdk.Deck(
        map_style=pdk.map_styles.CARTO_LIGHT,
        initial_view_state=view_state,
        layers=[saone_layer,icon_layer]
    )

    return deck
