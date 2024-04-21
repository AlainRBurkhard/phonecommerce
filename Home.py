import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config( page_title= 'e-Commerce Dashboard', page_icon = '📱', layout = 'wide')


daf=pd.read_csv('Data/merged_products_20240416.csv')
df = daf.copy()

df.rename(columns={'rating_100': 'score'}, inplace=True)
df_valid = df[df['delivery_time'].notna()]

###########################################################################################################
# Our Top

df_recommended = df_valid.sort_values(
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

df_best_deal = df_valid.sort_values(by=['price', 'delivery_time'])
df_best_deal.reset_index(drop=True, inplace=True)

df_best_deal.drop(columns='id', inplace=True)

df_best_deal.reset_index(drop=True, inplace=True)
df_best_deal.index += 1


df_best_deal['id'] = df_best_deal.index
cols = list(df_best_deal.columns)
cols = [cols[-1]] + cols[:-1]
df_best_deal = df_best_deal[cols]


###########################################################################################################

import streamlit as st
import pandas as pd

def main():
    st.title("Group 02 - CIP EN - Smartphones e-Commerce Recommendation")

    # Create a single tab
    tabs = st.tabs(["TipTopClub"])

    # Add content to the tab
    with tabs[0]:
        st.header("TipTop for You!")
        
        st.subheader("Select Your Preference")
        
        # Radio button for DataFrame selection
        df_choice = st.radio(
            "Choose an option:",
            options=('Our Top!', 'Best Deal $', 'Flash Delivery')
        )

        # Determine the DataFrame based on user selection
        if df_choice == 'Our Top!':
            selected_df = df_recommended
        elif df_choice == 'Best Deal $':
            selected_df = df_best_deal
        elif df_choice == 'Flash Delivery':
            selected_df = fastest_delivery_df
        
        # Display a selectbox with brand options from the selected DataFrame
        if 'selected_df' in locals():  # Check if selected_df is defined
            brand_choice = st.selectbox(
                "Select a brand from the chosen list:",
                options=pd.unique(selected_df['brand'].dropna())  # Get unique, non-null brand names
            )
            st.write(f"You selected the brand: {brand_choice}")
            
        # You can use `brand_choice` here for further operations, e.g., filtering the DataFrame by the selected brand
       
def process_data(df):
    # Placeholder function to represent some processing of the DataFrame
    # This could be data analysis, further filtering, or preparing data for visualization
    pass

if __name__ == "__main__":
    main()
