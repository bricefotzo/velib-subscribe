import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from api.external import get_dataset_info
from utils.helpers import results_to_df
# Configuration

DATASET_ID = "velib-disponibilite-en-temps-reel"


def render_ui(cities):
    """
    Render the Streamlit UI components.
    """
    st.title("Notification Vélib")
    city_id = st.selectbox("Choisissez votre ville", cities)
    station_name, time_slot, email = user_input(city_id)
    subscribe_button = st.button("S'abonner")

    return city_id, station_name, time_slot, email, subscribe_button


def user_input(city_id):
    """
    Collect user input from Streamlit UI.

    Args:
        city_id (str): Selected city ID

    Returns:
        tuple: station name, time slot, and email
    """
    stations_data = get_dataset_info(DATASET_ID, where=f'nom_arrondissement_communes like "{city_id}"', lang="fr")
    stations_df = results_to_df(stations_data)
    display_station_map(stations_df)

    station_name = st.selectbox("Choisissez votre station", stations_df["name"].tolist())
    time_slot = st.time_input("Heure de notification", step=300)
    email = st.text_input("Entrez votre adresse e-mail")

    return station_name, time_slot, email


def display_map(dataframe: pd.DataFrame) -> folium.Map:
    """
    Display a map with the stations

    Args:
        dataframe (pd.DataFrame): Stations dataframe

    Returns:
        folium.Map: Folium map
    """
    map_center = [dataframe.lat.mean(), dataframe.lon.mean()]
    folium_map = folium.Map(location=map_center, zoom_start=12, control_scale=True)

    for _, row in dataframe.iterrows():
        tooltip_content = (
            f"<b>Station:</b> {row['name']}<br>"
            f"<b>Places disponibles:</b> {row['numdocksavailable']}<br>"
            f"<b>Électriques disponibles:</b> {row['ebike']}<br>"
            f"<b>Mécaniques disponibles:</b> {row['mechanical']}"
        )
        folium.Marker([row['lat'], row['lon']], tooltip=tooltip_content).add_to(folium_map)

    return folium_map


def display_station_map(stations_df):
    """
    Display the station map using Folium.

    Args:
        stations_df (pd.DataFrame): Dataframe containing station information
    """
    map_ = display_map(stations_df)
    st_folium(map_, width=700)
