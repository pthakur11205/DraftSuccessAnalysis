import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a DataFrame
df = pd.read_csv('combined_draft_data_with_zScore.csv')

# Convert columns to appropriate data types if necessary
success_counts = df.groupby(['Team', 'Successful Pick']).size().unstack(fill_value=0)

# Calculate percentage of successful picks
success_counts['Success Rate %'] = success_counts[True] / (success_counts[True] + success_counts[False]) * 100

# Plot histogram
success_counts['Success Rate %'].plot(kind='bar', stacked=False)
plt.xlabel('Teams')
plt.ylabel('Successful Pick Percentage')
plt.title('Successful Pick Percentage by Teams since 1989')
plt.xticks(rotation=90, ha='right')
# plt.savefig('successful_pick_percentage_zScore.png')
plt.show()