###########################################################################################################
import streamlit as st
import pandas as pd
import numpy as np

###########################################################################################################
df = pd.read_csv('merged_products_20240416.csv')

df.rename(columns={'rating_100': 'score'}, inplace=True)
df_valid = df[df['delivery_time'].notna()]

###########################################################################################################
# Our recommendation

user_input = input("Please enter the model name you are interested in: ")
df_recommended = df_valid[df_valid['model'].str.lower() == user_input.lower()]

df_recommended = df_recommended.sort_values(
    by=['score', 'price', 'delivery_time', 'reviews_count', 'memory_GB', 'camera_MP'],
    ascending=[False, True, True, False, False, False])

df_recommended.reset_index(drop=True, inplace=True)

df_recommended.drop(columns='id', inplace=True)

# Reset the index to start from 1
df_recommended.reset_index(drop=True, inplace=True)
df_recommended.index += 1

# Create a new 'id' column from the index
df_recommended['id'] = df_recommended.index

# Optionally, move the 'id' column to the front if needed
cols = list(df_recommended.columns)
cols = [cols[-1]] + cols[:-1]  # This moves the last column (new 'id') to the first position
df_recommended = df_recommended[cols]

###########################################################################################################
# Fastest product

fastest_delivery_df = df_valid[df_valid['delivery_time'] <= 3.0]

user_input_1 = input("Please enter the model name you are interested in: ")
fastest_delivery_df = fastest_delivery_df[fastest_delivery_df['model'].str.lower() == user_input_1.lower()]

# Sort the filtered DataFrame by 'model' and 'price'
fastest_delivery_df = fastest_delivery_df.sort_values(by=['delivery_time', 'price'])
fastest_delivery_df.reset_index(drop=True, inplace=True)

fastest_delivery_df.drop(columns='id', inplace=True)

# Reset the index to start from 1
fastest_delivery_df.reset_index(drop=True, inplace=True)
fastest_delivery_df.index += 1

# Create a new 'id' column from the index
fastest_delivery_df['id'] = fastest_delivery_df.index

# Optionally, move the 'id' column to the front if needed
cols = list(fastest_delivery_df.columns)
cols = [cols[-1]] + cols[:-1]  # This moves the last column (new 'id') to the first position
fastest_delivery_df = fastest_delivery_df[cols]

###########################################################################################################
# Best price product

user_input_2 = input("Please enter the model name you are interested in: ")

# Filter the DataFrame for the user-specified model
filtered_df = df_valid[df_valid['model'].str.lower() == user_input_2.lower()]

# Sort the filtered DataFrame by 'model' and 'price'
df_best_deal = filtered_df.sort_values(by=['model', 'price', 'delivery_time'])
df_best_deal.reset_index(drop=True, inplace=True)

df_best_deal.drop(columns='id', inplace=True)

# Reset the index to start from 1
df_best_deal.reset_index(drop=True, inplace=True)
df_best_deal.index += 1

# Create a new 'id' column from the index
df_best_deal['id'] = df_best_deal.index

# Optionally, move the 'id' column to the front if needed
cols = list(df_best_deal.columns)
cols = [cols[-1]] + cols[:-1]  # This moves the last column (new 'id') to the first position
df_best_deal = df_best_deal[cols]
