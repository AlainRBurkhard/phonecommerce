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

        dataframes = {
            'Our Top!': df_recommended,
            'Best Deal $': df_best_deal,
            'Flash Delivery': fastest_delivery_df
        }

        selected_df = dataframes[df_choice] if df_choice in dataframes else None

        if selected_df is not None:
            col1, col2, col3 = st.columns(3)  # Create three columns for the select boxes

            # Sort brands by frequency
            brand_counts = selected_df['brand'].dropna().value_counts().index.tolist()
            with col1:  # First column for brands
                brand_choice = st.selectbox(
                    "Select a brand:",
                    options=brand_counts,
                    key='brand_select'
                )

            df_filtered_by_brand = selected_df[selected_df['brand'] == brand_choice]

            # Sort models by frequency within the selected brand
            with col2:  # Second column for models
                if not df_filtered_by_brand.empty:
                    model_counts = df_filtered_by_brand['model'].dropna().value_counts().index.tolist()
                    model_choice = st.selectbox(
                        "Select a model:",
                        options=model_counts,
                        key='model_select'
                    )

            df_filtered_by_model = df_filtered_by_brand[df_filtered_by_brand['model'] == model_choice] if not df_filtered_by_brand.empty else pd.DataFrame()

            with col3:  # Third column for memory
                if not df_filtered_by_model.empty:
                    memory_options = ['Any'] + list(pd.unique(df_filtered_by_model['memory_GB'].dropna()))
                    memory_choice = st.selectbox(
                        "Select memory (optional):",
                        options=memory_options,
                        key='memory_select'
                    )

            # Adjust DataFrame based on optional memory choice
            if memory_choice != 'Any' and not df_filtered_by_model.empty:
                df_final = df_filtered_by_model[df_filtered_by_model['memory_GB'] == memory_choice]
            else:
                df_final = df_filtered_by_model

            # Optionally display the final DataFrame below the columns if needed
            if not df_final.empty:
                st.dataframe(df_final)

if __name__ == "__main__":
    main()
