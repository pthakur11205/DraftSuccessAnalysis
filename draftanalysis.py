import pandas as pd

# Read the data
df = pd.read_csv('OKCdraft_data.csv')

# Convert necessary columns to numeric
numeric_cols = ['VORP', 'WS', 'BPM', 'PPG', 'TRB', 'AST', 'FG%', '3P%', 'FT%']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Drop rows with NaN values in key metrics
df = df.dropna(subset=numeric_cols)

# Example of evaluating draft success
# Calculate average VORP and WS by draft position
avg_vorp_by_position = df.groupby('Pk')['VORP'].mean()
avg_ws_by_position = df.groupby('Pk')['WS'].mean()

print("Average VORP by Draft Position:")
print(avg_vorp_by_position)

print("Average WS by Draft Position:")
print(avg_ws_by_position)

# Analyze success relative to draft position
df['Draft Success'] = df.apply(lambda row: row['VORP'] > avg_vorp_by_position[row['Pk']] and row['WS'] > avg_ws_by_position[row['Pk']], axis=1)

# Print out successful draft picks
successful_picks = df[df['Draft Success']]
print("Successful Draft Picks:")
print(successful_picks[['Player', 'Pk', 'VORP', 'WS']])
