import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Title
st.write("""
# Visualize log files
## Upload
Upload logged data files that were collected during survey (.txt).
""")

# Upload files and read dataframes
files = st.file_uploader('Upload datafile(s)',
                          accept_multiple_files=True
                        )

dfs, options = [], []
for file in files:

    # Grab data
    df = pd.read_csv(file).dropna(subset=['WGS84_LON', 'WGS84_LON'])
    lon, lat = df['WGS84_LON'].values, df['WGS84_LAT'].values

    # Store
    options.append(file.name)
    file.seek(0)  # reset
    dfs.append(df)

# Create color palette
rgbs = [[84, 71, 140], [44, 105, 154], [4, 139, 168], [13, 179, 158], [22, 219, 147], [131, 227, 119], [185, 231, 105], [239, 234, 90], [241, 196, 83], [242, 158, 76]]

layers = []
if dfs:
    
    # Create multi selector for filenames
    opts = [options.index(o) for o in st.multiselect('Select datafile(s) to visualize', options, default=options)]
    sub = st.number_input('Resample every', 1, 20, 10, format='%i')

    # Calculate viewport of entire dataset
    for ii, num in enumerate(opts):
        df_ = dfs[num]
        if ii == 0:
            df_['survey'] = ii
            df = df_.copy()
        else:
            df_['survey'] = ii
            df = df.append(df_)
            df.append(df_)
    
        # Construct layers
        layers.append(pdk.Layer('ScatterplotLayer',
                                df_[['GPS_FIX', 'WGS84_LON', 'WGS84_LAT']], 
                                get_position=['WGS84_LON', 'WGS84_LAT'],
                                get_radius=2,
                                get_fill_color=rgbs[ii]
                                )
                    )
    
    viewport = pdk.data_utils.compute_view(points=df[['WGS84_LON', 'WGS84_LAT']])

    st.write("""
    ## Visualization
    GPS data is plotted on top of OpenStreetMap for reference.
    """)
    # Visualize
    st.pydeck_chart(
        pdk.Deck(layers,
                 initial_view_state=viewport,
                 map_style='mapbox://styles/mapbox/satellite-v9'
                 )
        )
