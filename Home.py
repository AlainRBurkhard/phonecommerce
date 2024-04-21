import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config( page_title= 'e-Commerce Dashboard', page_icon = '📱', layout = 'wide')

###########################################################################################################

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

def display_product_details(df):  ## details of the result
    if not df.empty:
        # Extract the first row of the DataFrame
        product = df.iloc[0]

        st.markdown("###")  

        
        with st.container():
            st.markdown("#### Our Result")  
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

            with col1:
                st.write(f"**Source:**")
                st.write(product['source'])

            with col2:
                st.write(f"**Brand:**")
                st.write(product['brand'])

            with col3:
                st.write(f"**Model:**")
                st.write(product['model'])

            with col4:
                st.write(f"**Memory:**")
                st.write(f"{product['memory_GB']} GB")

            with col5:
                st.write(f"**Color:**")
                st.write(product['color'])

            with col6:
                st.write(f"**Score:**")
                st.write(product['score'])

            with col7:
                st.write(f"**Price:**")
                st.write(f"${product['price']:.2f}")

            with col8:
                st.write(f"**Delivery:**")
                st.write(f"{product['delivery_time']} days")

            with col9:
                st.write(f"**Link:**")
                url = product['source']
                st.markdown(f"[Link]({url})", unsafe_allow_html=True)

            st.markdown("""
            <style>
            .stContainer {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

def display_remaining_data(df):
    if not df.empty:
        st.markdown("###") 
        for index, row in df.iterrows():
            cols = st.columns(9)
            cols[0].write(row['source'])
            cols[1].write(row['brand'])
            cols[2].write(row['model'])
            cols[3].write(f"{row['memory_GB']} GB")
            cols[4].write(row['color'])
            cols[5].write(row['score'])
            cols[6].write(f"${row['price']:.2f}")
            cols[7].write(f"{row['delivery_time']} days")
            cols[8].markdown(f"[Link]({row['source']})", unsafe_allow_html=True)

def main():
    st.title("Group 02 - CIP EN - Smartphones e-Commerce Recommendation")

    tabs = st.tabs(["TipTopClub", "Explanation"])


    with tabs[0]:
        st.header("TipTop for You!")
        st.subheader("Select Your Preference")

        df_choice = st.radio(
            "Choose an option:",
            options=('Our Top!', 'Best Deal $', 'Flash Delivery'),
            key='df_choice'
        )

        dataframes = {
            'Our Top!': df_recommended,
            'Best Deal $': df_best_deal,
            'Flash Delivery': fastest_delivery_df
        }

        selected_df = dataframes[df_choice] if df_choice in dataframes else None

        if selected_df is not None:
            col1, col2, col3 = st.columns(3)  

            brand_counts = selected_df['brand'].dropna().value_counts().index.tolist()
            with col1:  # First column for brands
                brand_choice = st.selectbox(
                    "Select a brand:",
                    options=brand_counts,
                    key='brand_select'
                )

            df_filtered_by_brand = selected_df[selected_df['brand'] == brand_choice]

            with col2:  # Second column 
                if not df_filtered_by_brand.empty:
                    model_counts = df_filtered_by_brand['model'].dropna().value_counts().index.tolist()
                    model_choice = st.selectbox(
                        "Select a model:",
                        options=model_counts,
                        key='model_select'
                    )

            df_filtered_by_model = df_filtered_by_brand[df_filtered_by_brand['model'] == model_choice] if not df_filtered_by_brand.empty else pd.DataFrame()

            with col3:  
                if not df_filtered_by_model.empty:
                    memory_options = ['Any'] + list(pd.unique(df_filtered_by_model['memory_GB'].dropna()))
                    memory_choice = st.selectbox(
                        "Select memory (optional):",
                        options=memory_options,
                        key='memory_select'
                    )

            if memory_choice != 'Any' and not df_filtered_by_model.empty:
                df_final = df_filtered_by_model[df_filtered_by_model['memory_GB'] == memory_choice]
            else:
                df_final = df_filtered_by_model

            if not df_final.empty:
                display_product_details(df_final.iloc[[0]])  # Display first row details
                st.markdown("### Check it out too")
                display_remaining_data(df_final.iloc[1:])
    
    with tabs[1]: #tab to explain what is done
        st.header("Explanation of Sorting Criteria")
        st.markdown("""
        **Our Top:**
        - Sorted primarily by `score` (highest to lowest).
        - Secondary sorting by `price` (lowest to highest) and `delivery time` (shortest to longest).

        **Fastest Delivery:**
        - Sorted by `delivery time` (shortest to longest).
        - Secondary sorting by `price` (lowest to highest).

        **Best Deal:**
        - Sorted by `price` (lowest to highest).
        - Secondary sorting by `delivery time` (shortest to longest).

        These criteria ensure that the results are tailored to highlight the most appealing products based on the selected category.
        """)

if __name__ == "__main__":
    main()
