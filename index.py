import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a DataFrame
df = pd.read_csv('OKCdraft_data.csv')

# Convert columns to appropriate data types if necessary
df['BPM'] = pd.to_numeric(df['BPM'], errors='coerce')
df['Pk'] = pd.to_numeric(df['Pk'], errors='coerce')

# Drop rows with NaN values in 'PTS' or 'Pk'
df = df.dropna(subset=['BPM', 'Pk'])

# Plot points vs draft positions
plt.figure(figsize=(12, 8))
plt.scatter(df['Pk'], df['BPM'], color='blue')

# Annotate each point with the player's name
for i, row in df.iterrows():
    plt.annotate(row['Player'], (row['Pk'], row['BPM']), textcoords="offset points", xytext=(0,5), ha='center')

plt.xlabel('Draft Position')
plt.ylabel('BPM')
plt.title('BPM vs. Draft Position for OKC Thunder Draft Picks')
plt.grid(True)
plt.show()
