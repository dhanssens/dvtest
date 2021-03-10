import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Title
st.write("""
# FILE VISUALIZER
## Upload datafile(s)
Upload data files that were collected during survey (.txt).
""")

# Upload files and read dataframes
files = st.file_uploader('Upload datafile(s)',
                          accept_multiple_files=True
                        )

dfs = []
options = []
for file in files:

    # Grab data
    df = pd.read_csv(file).dropna(subset=['WGS84_LON', 'WGS84_LON'])
    lon, lat = df['WGS84_LON'].values, df['WGS84_LAT'].values

    # Store
    options.append(file.name)
    file.seek(0)  # reset
    dfs.append(df)

layers = []
if dfs:

    # Calculate viewport of entire dataset
    for ii, df_ in enumerate(dfs):
        if ii == 0:
            df_['survey'] = ii
            df = df_.copy()
        else:
            df_['survey'] = ii
            df = df.append(df_)
            df.append(df_)
    viewport = pdk.data_utils.compute_view(points=df[['WGS84_LON', 'WGS84_LAT']])

    # Construct layers
    layers.append(pdk.Layer('ScatterplotLayer',
                      df[['GPS_FIX', 'WGS84_LON', 'WGS84_LAT']], 
                      get_position=['WGS84_LON', 'WGS84_LAT'],
                      get_radius=2,
                      get_fill_color=[180, 0, 200]
                      )
    )

    st.write("""
    ## Data visualization
    GPS data is plotted on top of OpenStreetMap for reference.
    """)
    # Visualize
    st.pydeck_chart(
        pdk.Deck(
            layers,
            initial_view_state=viewport,
            map_style='mapbox://styles/mapbox/satellite-v9'
            )
        )
