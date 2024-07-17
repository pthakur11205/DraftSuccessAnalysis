import pandas as pd
import os

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

# Calculate median and standard deviation for VORP, WS, and BPM by year
medians_by_year = df_combined.groupby('Year').agg({'VORP': 'median', 'WS': 'median', 'BPM': 'median'})
std_by_year = df_combined.groupby('Year').agg({'VORP': 'std', 'WS': 'std', 'BPM': 'std'})

# Determine draft success relative to each draft year
def is_successful_pick(row):
    year = row['Year']
    if year in medians_by_year.index:
        vorp_median, vorp_std = medians_by_year.loc[year, 'VORP'], std_by_year.loc[year, 'VORP']
        ws_median, ws_std = medians_by_year.loc[year, 'WS'], std_by_year.loc[year, 'WS']
        bpm_median, bpm_std = medians_by_year.loc[year, 'BPM'], std_by_year.loc[year, 'BPM']
        
        return (row['VORP'] > vorp_median + 1.5 * vorp_std) and (row['WS'] > ws_median + 1.5 * ws_std) and (row['BPM'] > bpm_median + 1.5 * bpm_std)
    return False

df_combined['Successful Pick'] = df_combined.apply(is_successful_pick, axis=1)

# Print out successful draft picks
successful_picks = df_combined[df_combined['Successful Pick']]
print("Successful Draft Picks:")
print(successful_picks[['Player', 'Team', 'Pk', 'VORP', 'WS', 'BPM']])

# Save the combined DataFrame to a new CSV file
df_combined.to_csv('combined_draft_data.csv', index=False)
