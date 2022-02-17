import pydeck as pdk

def get_deck(stations,station_id):

    lat = stations.loc[station_id,'lat']
    lon = stations.loc[station_id,'lon']

    deck = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon,
            zoom=11,
            pitch=0,
            )
    )

    return deck
