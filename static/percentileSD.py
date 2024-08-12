import pandas as pd
import numpy as np
import os

folder_path = 'TeamDraftData'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
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

# Calculate median and standard deviation for VORP, WS, and BPM by year
medians_by_year = df_combined.groupby('Year').agg({'VORP': 'median', 'WS': 'median', 'BPM': 'median'})
std_by_year = df_combined.groupby('Year').agg({'VORP': 'std', 'WS': 'std', 'BPM': 'std'})

# Calculate percentile ranks for each stat within each draft year
def percentile_rank(series):
    return series.rank(pct=True)

stats_for_percentile = ['VORP', 'WS', 'BPM']

for stat in stats_for_percentile:
    df_combined[f'{stat}_Percentile'] = df_combined.groupby('Year')[stat].transform(percentile_rank)

# Calculate percentile ranks for each stat within each draft position
for stat in stats_for_percentile:
    df_combined[f'{stat}_PositionPercentile'] = df_combined.groupby('Pk')[stat].transform(percentile_rank)

# Round percentiles to two decimal places
percentile_cols = [f'{stat}_Percentile' for stat in stats_for_percentile] + \
                  [f'{stat}_PositionPercentile' for stat in stats_for_percentile]
df_combined[percentile_cols] = df_combined[percentile_cols].round(2)

# Define success criteria
def is_successful_pick(row):
    # Original criteria
    year = row['Year']
    if year in medians_by_year.index:
        vorp_median, vorp_std = medians_by_year.loc[year, 'VORP'], std_by_year.loc[year, 'VORP']
        ws_median, ws_std = medians_by_year.loc[year, 'WS'], std_by_year.loc[year, 'WS']
        bpm_median, bpm_std = medians_by_year.loc[year, 'BPM'], std_by_year.loc[year, 'BPM']
        
        original_criteria = (
            (row['VORP'] > vorp_median + 1.25 * vorp_std) and 
            (row['WS'] > ws_median + 1.25 * ws_std) and 
            (row['BPM'] > bpm_median + 1.25 * bpm_std)
        )
    else:
        original_criteria = False
    
    # New percentile criteria
    percentile_criteria = all(
        row[f'{stat}_Percentile'] > 0.7 and row[f'{stat}_PositionPercentile'] > 0.7
        for stat in ['VORP', 'WS', 'BPM']
    )
    
    # Combined criteria (player must meet either the original or the new percentile criteria)
    return original_criteria or percentile_criteria

df_combined['Successful Pick'] = df_combined.apply(is_successful_pick, axis=1)

# Print out successful draft picks
successful_picks = df_combined[df_combined['Successful Pick']]
print("Successful Draft Picks:")
print(successful_picks[['Player', 'Team', 'Pk', 'VORP', 'WS', 'BPM', 'VORP_Percentile', 'WS_Percentile', 'BPM_Percentile']])

# Save the combined DataFrame to a new CSV file
df_combined.to_csv('combined_draft_data_with_percentiles.csv', index=False)
