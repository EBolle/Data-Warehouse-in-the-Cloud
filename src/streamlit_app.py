"""Contains all the underlying code for the streamlit app, please refer to the README how to launch the app."""

# setup
import pandas as pd
import psycopg2
from settings import DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
import streamlit as st

conn = psycopg2.connect(f"postgresql://{DWH_DB_USER}:{DWH_DB_PASSWORD}@{DWH_ENDPOINT}:{DWH_PORT}/{DWH_DB}")

# streamlit app

st.title('Sparkify insights powered by Streamlit')

st.subheader('Where are the artists located?')


@st.cache
def load_artists_data():
    artists = pd.read_sql("SELECT * from artists", con=conn)
    row_mask = artists[['latitude', 'longitude']].notna().all(axis=1)
    artists = artists.loc[row_mask, ['latitude', 'longitude']]

    return artists


artists_data_load_state = st.text('Loading artists data...')
artists_data = load_artists_data()
artists_data_load_state.text('Loading artists data...done!')


st.map(artists_data)
