import pandas as pd

# Define file paths
okc_file_path = 'OKCdraft_data.csv'
kings_file_path = 'Kingsdraft_data.csv'

# Read the OKC Thunder draft data
df_okc = pd.read_csv(okc_file_path)

# Read the Kings' player data
df_kings = pd.read_csv(kings_file_path)

# Add a column to indicate the team
df_okc['Team'] = 'OKC Thunder'
df_kings['Team'] = 'Kings'

# Concatenate the DataFrames
df_combined = pd.concat([df_okc, df_kings], ignore_index=True)

# Convert columns to appropriate data types if necessary
numeric_cols = ['VORP', 'WS', 'BPM', 'PTS', 'TRB', 'AST', 'FG%', '3P%', 'FT%']
df_combined[numeric_cols] = df_combined[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values in key metrics
df_combined = df_combined.dropna(subset=numeric_cols)

# Example analysis: Average VORP and WS by draft position across both teams
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
print(successful_picks[['Player', 'Team', 'Pk', 'VORP', 'WS']])

# Optional: Save the combined DataFrame to a new CSV file
df_combined.to_csv('combined_draft_data.csv', index=False)
