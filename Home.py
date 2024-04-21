import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.image as mpimg
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
from folium import plugins
import streamlit as st

st.set_page_config( page_title= 'e-Commerce Dashboard', page_icon = '📱', layout = 'wide')


from functions import sidebar

def sidebar(df):
    
    
    st.sidebar.markdown('# Smartphones Recommendation')
    st.sidebar.markdown('## Fast Home Food')
    st.sidebar.markdown("""---""")

    date_slider = st.sidebar.slider(
        'Date',
        value=pd.Timestamp('2022-04-13').to_pydatetime(),
        min_value=pd.Timestamp('2022-02-11').to_pydatetime(),
        max_value=pd.Timestamp('2022-04-06').to_pydatetime(),
        format='YYYY-MM-DD'
        )
    st.sidebar.markdown("""---""")

    ## ---- Traffic filter ----##

    traffic_conditions = st.sidebar.multiselect(
        'Traffic density',
        ['Low', 'Medium', 'High', 'Jam'],
        default=['Low', 'Medium', 'High', 'Jam'])

    st.sidebar.markdown("""---""")

    ## ---- Weather filter ----##

    Weatherconditions_filter = st.sidebar.multiselect(
        'Weathercondition',
        ['Sunny', 'Stormy', 'Cloudy', 'Sandstorms', 'Windy','Fog'],
        default=['Sunny', 'Stormy', 'Cloudy', 'Sandstorms', 'Windy','Fog'])

    st.sidebar.markdown("""---""")
    st.sidebar.markdown('#### Powered by Ramon Burkhard')

    #---------setting the filters-------------#
    
    # Date filter
    selected_lines = df['Order_Date'] < date_slider
    df = df.loc[selected_lines, :]

    #traffic filter
    selected_lines = df['Road_traffic_density'].isin(traffic_conditions)
    df = df.loc[selected_lines,:]

    # #weathercondition filter
    selected_lines = df['Weatherconditions'].isin(Weatherconditions_filter)
    df = df.loc[selected_lines,:]
    
    return df

df = sidebar(df)


tab1 = st.tabs( ['TipTopClub']) 

with tab1:
    
    with st.container():
        #orders per day
        st.header('TipTop for You!')