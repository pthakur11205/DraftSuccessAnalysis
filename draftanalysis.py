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

# Average VORP, WS, and BPM by draft position across all teams
avg_vorp_by_position = df_combined.groupby('Pk')['VORP'].mean()
avg_ws_by_position = df_combined.groupby('Pk')['WS'].mean()
avg_bpm_by_position = df_combined.groupby('Pk')['BPM'].mean()

print("Average VORP by Draft Position:")
print(avg_vorp_by_position)
print("")
print("Average WS by Draft Position:")
print(avg_ws_by_position)
print("")
print("Average BPM by Draft Position:")
print(avg_bpm_by_position)

# Determine draft success relative to combined data
df_combined['Successful Pick'] = df_combined.apply(
    lambda row: row['VORP'] > avg_vorp_by_position.get(row['Pk'], 0) and row['WS'] > avg_ws_by_position.get(row['Pk'], 0) and row['BPM'] >
    avg_bpm_by_position.get(row['Pk'], 0),
    axis=1
)

# Print out successful draft picks
successful_picks = df_combined[df_combined['Successful Pick']]
print("Successful Draft Picks:")
print(successful_picks[['Player', 'Team', 'Pk', 'VORP', 'WS', 'BPM']])

# Save the combined DataFrame to a new CSV file
df_combined.to_csv('combined_draft_data.csv', index=False)
