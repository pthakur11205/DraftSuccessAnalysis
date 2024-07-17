import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a DataFrame
df = pd.read_csv('combined_draft_data.csv')

# Convert columns to appropriate data types if necessary
success_counts = df.groupby(['Team', 'Successful Pick']).size().unstack(fill_value=0)

# Calculate percentage of successful picks
success_counts['Success Rate %'] = success_counts[True] / (success_counts[True] + success_counts[False]) * 100

# Plot histogram
success_counts['Success Rate %'].plot(kind='bar', stacked=False)
plt.xlabel('Teams')
plt.ylabel('Successful Pick Percentage')
plt.title('Successful Pick Percentage by Team')
plt.xticks(rotation=15, ha='right')
plt.show()