from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Read Z-score data
    df_zscore = pd.read_csv('./combined_draft_data/combined_draft_data_with_zScore.csv')
    success_counts_zscore = df_zscore.groupby(['Team', 'Successful Pick']).size().unstack(fill_value=0)
    success_counts_zscore['Success Rate %'] = success_counts_zscore[True] / (success_counts_zscore[True] + success_counts_zscore[False]) * 100
    success_rate_dict_zscore = success_counts_zscore['Success Rate %'].to_dict()

    # Read percentile data
    df_percentile = pd.read_csv('./combined_draft_data/combined_draft_data_with_percentiles.csv')
    success_counts_percentile = df_percentile.groupby(['Team', 'Successful Pick']).size().unstack(fill_value=0)
    success_counts_percentile['Success Rate %'] = success_counts_percentile[True] / (success_counts_percentile[True] + success_counts_percentile[False]) * 100
    success_rate_dict_percentile = success_counts_percentile['Success Rate %'].to_dict()

    return render_template('index.html', success_rate_zscore=success_rate_dict_zscore, success_rate_percentile=success_rate_dict_percentile)

if __name__ == '__main__':
    app.run(debug=True)
