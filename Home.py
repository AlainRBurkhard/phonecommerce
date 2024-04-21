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

df_recommended = df_recommended.dropna(subset=['score'])

df_recommended = df_recommended[df_recommended['score'] != 0]

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

# Sample DataFrame definitions (you'll replace these with your actual DataFrame imports)
# Define sample DataFrames here or import them before using them in the app.
# df_recommended, df_best_deal, fastest_delivery_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

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
            options=('Our Top!', 'Best Deal $', 'Flash Delivery'),
            key='df_choice'
        )

        # Initialize session state for brand, model, and memory
        if 'brand' not in st.session_state:
            st.session_state.brand = None
        if 'model' not in st.session_state:
            st.session_state.model = None
        if 'memory' not in st.session_state:
            st.session_state.memory = None

        dataframes = {
            'Our Top!': df_recommended,
            'Best Deal $': df_best_deal,
            'Flash Delivery': fastest_delivery_df
        }

        selected_df = dataframes[df_choice] if df_choice in dataframes else None

        if selected_df is not None:
            brand_options = pd.unique(selected_df['brand'].dropna())
            brand_choice = st.selectbox(
                "Select a brand:",
                options=brand_options,
                index=brand_options.tolist().index(st.session_state.brand) if st.session_state.brand in brand_options else 0,
                key='brand'
            )
            st.session_state.brand = brand_choice  # Update session state

            df_filtered_by_brand = selected_df[selected_df['brand'] == brand_choice]

            if not df_filtered_by_brand.empty:
                model_options = pd.unique(df_filtered_by_brand['model'].dropna())
                model_choice = st.selectbox(
                    "Select a model:",
                    options=model_options,
                    index=model_options.tolist().index(st.session_state.model) if st.session_state.model in model_options else 0,
                    key='model'
                )
                st.session_state.model = model_choice  # Update session state

                df_filtered_by_model = df_filtered_by_brand[df_filtered_by_brand['model'] == model_choice]

                if not df_filtered_by_model.empty:
                    memory_options = ['Any'] + list(pd.unique(df_filtered_by_model['memory_GB'].dropna()))
                    memory_choice = st.selectbox(
                        "Select memory (optional):",
                        options=memory_options,
                        index=memory_options.index(st.session_state.memory) if st.session_state.memory in memory_options else 0,
                        key='memory'
                    )
                    st.session_state.memory = memory_choice  # Update session state

                    if memory_choice != 'Any':
                        df_final = df_filtered_by_model[df_filtered_by_model['memory_GB'] == memory_choice]
                    else:
                        df_final = df_filtered_by_model

                    st.dataframe(df_final)

if __name__ == "__main__":
    main()
