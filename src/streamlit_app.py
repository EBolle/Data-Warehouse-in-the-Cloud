"""Contains all the underlying code for the streamlit app, please refer to the README how to launch the app."""

# setup
import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import seaborn as sns
from settings import DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT, DWH_DB
import streamlit as st

conn = psycopg2.connect(f"postgresql://{DWH_DB_USER}:{DWH_DB_PASSWORD}@{DWH_ENDPOINT}:{DWH_PORT}/{DWH_DB}")

# streamlit app

st.title('Sparkify insights powered by Streamlit')

st.subheader('Where are the artists located?')

def load_artists_data():
    artists = pd.read_sql("SELECT * from artists", con=conn)
    row_mask = artists[['latitude', 'longitude']].notna().all(axis=1)
    artists = artists.loc[row_mask, ['latitude', 'longitude']]

    return artists

artists_data_load_state = st.text('Loading artists data...')
artists_data = load_artists_data()
artists_data_load_state.text('Loading artists data...done!')

st.map(artists_data)


st.subheader('Is there a difference in user activity between paying and non-paying customers?')

def load_songplays_data():
    songplays = pd.read_sql("SELECT * from songplays", parse_dates=['start_time'], con=conn)
    songplays['start_time'] = songplays['start_time'].dt.date
    songplays_wide = songplays[['start_time', 'level']].groupby(['start_time', 'level']).agg('size').reset_index()
    songplays_wide.columns = ['date', 'level', 'users']
    songplays_wide = songplays_wide.pivot("date", "level", "users")

    return songplays_wide

songplays_data_load_state = st.text('Loading songplays data...')
songplays = load_songplays_data()
songplays_data_load_state.text('Loading songplays data...done!')

fig, ax = plt.subplots(figsize=(16, 8))

sns.lineplot(ax=ax, data=songplays)
ax.set_xlabel('date', fontsize=14)
ax.set_ylabel('songs played', fontsize=14)
ax.set_title('Paid users are more active and seem to follow a certain pattern', fontsize=18)
ax.tick_params(axis='x', labelrotation=45)

st.pyplot(fig)
