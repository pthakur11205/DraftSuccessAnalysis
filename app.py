from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read data
    df = pd.read_csv('combined_draft_data_with_zScore.csv')
    
    # Convert columns to appropriate data types if necessary
    success_counts = df.groupby(['Team', 'Successful Pick']).size().unstack(fill_value=0)
    
    # Calculate percentage of successful picks
    success_counts['Success Rate %'] = success_counts[True] / (success_counts[True] + success_counts[False]) * 100
    
    # Convert to dictionary for rendering in the template
    success_rate_dict = success_counts['Success Rate %'].to_dict()
    
    return render_template('index.html', success_rate=success_rate_dict)

if __name__ == '__main__':
    app.run(debug=True)
