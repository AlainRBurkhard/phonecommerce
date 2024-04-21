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


daf=pd.read_csv('Data/merged_products_20240416.csv.csv')
df = daf.copy()

df.rename(columns={'rating_100': 'score'}, inplace=True)
df_valid = df[df['delivery_time'].notna()]

###########################################################################################################
# Our Top

df_recommended = df_recommended.sort_values(
    by=['score', 'price', 'delivery_time', 'reviews_count', 'memory_GB', 'camera_MP'],
    ascending=[False, True, True, False, False, False])

df_recommended.reset_index(drop=True, inplace=True)

df_recommended.drop(columns='id', inplace=True)

df_recommended.reset_index(drop=True, inplace=True)
df_recommended.index += 1
df_recommended['id'] = df_recommended.index


cols = list(df_recommended.columns)
cols = [cols[-1]] + cols[:-1]  
df_recommended = df_recommended[cols]

###########################################################################################################
# Fastest at you

fastest_delivery_df = df_valid[df_valid['delivery_time'] <= 3.0]

fastest_delivery_df = fastest_delivery_df.sort_values(by=['delivery_time', 'price'])
fastest_delivery_df.reset_index(drop=True, inplace=True)

fastest_delivery_df.drop(columns='id', inplace=True)

fastest_delivery_df.reset_index(drop=True, inplace=True)
fastest_delivery_df.index += 1

fastest_delivery_df['id'] = fastest_delivery_df.index

cols = list(fastest_delivery_df.columns)
cols = [cols[-1]] + cols[:-1]  
fastest_delivery_df = fastest_delivery_df[cols]

###########################################################################################################
# Best deal $

df_best_deal = filtered_df.sort_values(by=['model', 'price', 'delivery_time'])
df_best_deal.reset_index(drop=True, inplace=True)

df_best_deal.drop(columns='id', inplace=True)

df_best_deal.reset_index(drop=True, inplace=True)
df_best_deal.index += 1


df_best_deal['id'] = df_best_deal.index
cols = list(df_best_deal.columns)
cols = [cols[-1]] + cols[:-1]
df_best_deal = df_best_deal[cols]


###########################################################################################################
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
