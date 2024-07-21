import pandas as pd
import numpy as np
import os
from scipy.stats import zscore

# Define the folder path
folder_path = 'TeamDraftData'

# Get all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Initialize an empty list to store DataFrames
dfs = []

# Read each CSV file and add a column indicating the team
for file in csv_files:
    team_name = file.replace('draft_data.csv', '').replace('_', ' ').strip()
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df['Team'] = team_name
    dfs.append(df)

# Concatenate the DataFrames
df_combined = pd.concat(dfs, ignore_index=True)

# Convert columns to appropriate data types if necessary
numeric_cols = ['VORP', 'WS', 'BPM', 'PTS', 'TRB', 'AST', 'FG%', '3P%', 'FT%']
df_combined[numeric_cols] = df_combined[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values in key metrics
df_combined = df_combined.dropna(subset=numeric_cols)

# Calculate z-scores within each draft year
for stat in ['VORP', 'WS', 'BPM']:
    df_combined[f'{stat}_Z_Year'] = df_combined.groupby('Year')[stat].transform(zscore)

# Calculate z-scores within each draft position
for stat in ['VORP', 'WS', 'BPM']:
    df_combined[f'{stat}_Z_Position'] = df_combined.groupby('Pk')[stat].transform(zscore)

# Define weights for each metric
weights = {'VORP_Z_Year': 0.2, 'WS_Z_Year': 0.15, 'BPM_Z_Year': 0.15,
           'VORP_Z_Position': 0.2, 'WS_Z_Position': 0.15, 'BPM_Z_Position': 0.15}

# Calculate weighted score for each player
df_combined['Weighted_Score'] = (
    df_combined['VORP_Z_Year'] * weights['VORP_Z_Year'] + 
    df_combined['WS_Z_Year'] * weights['WS_Z_Year'] + 
    df_combined['BPM_Z_Year'] * weights['BPM_Z_Year'] +
    df_combined['VORP_Z_Position'] * weights['VORP_Z_Position'] + 
    df_combined['WS_Z_Position'] * weights['WS_Z_Position'] + 
    df_combined['BPM_Z_Position'] * weights['BPM_Z_Position']
)

# Round percentiles and weighted scores to two decimal places
df_combined = df_combined.round({'VORP_Z_Year': 2, 'WS_Z_Year': 2, 'BPM_Z_Year': 2, 
                                 'VORP_Z_Position': 2, 'WS_Z_Position': 2, 'BPM_Z_Position': 2, 
                                 'Weighted_Score': 2})

# Define success threshold 
success_threshold = 0.75
df_combined['Successful Pick'] = df_combined['Weighted_Score'] >= success_threshold

# Print out successful draft picks
successful_picks = df_combined[df_combined['Successful Pick']]
print("Successful Draft Picks:")
print(successful_picks[['Player', 'Team', 'Pk', 'VORP', 'WS', 'BPM', 'Weighted_Score']])

# Save the combined DataFrame to a new CSV file
df_combined.to_csv('combined_draft_data_with_weighted_scores.csv', index=False)
