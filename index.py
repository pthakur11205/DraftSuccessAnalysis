import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a DataFrame
df = pd.read_csv('draft_data.csv')

# Convert columns to appropriate data types if necessary
df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')
df['Pk'] = pd.to_numeric(df['Pk'], errors='coerce')

# Drop rows with NaN values in 'PTS' or 'Pk'
df = df.dropna(subset=['PTS', 'Pk'])

# Plot points vs draft positions
plt.figure(figsize=(10, 6))
plt.scatter(df['Pk'], df['PTS'], color='blue')
plt.xlabel('Draft Position')
plt.ylabel('Points')
plt.title('Points vs. Draft Position for OKC Thunder Draft Picks')
plt.grid(True)
plt.show()
