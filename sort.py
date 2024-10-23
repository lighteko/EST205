import pandas as pd

# fetch csv file
data = pd.read_csv('./res/analysis/thredup_google_play_version_rating.csv')
data = data.sort_values(by='Version', ascending=False)
# save to csv
data.to_csv('./res/analysis/thredup_google_play_version_rating_sorted.csv', index=False)
