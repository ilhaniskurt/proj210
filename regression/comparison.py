import pandas as pd
from sklearn.metrics import mean_squared_error

# Load the actual data for the first 4 months of 2023
actual_data = pd.read_csv('actual_data_January_April_2023.csv', usecols=['Country', 'January', 'February', 'March', 'April'])

# Load the predicted data for the first 4 months of 2023
predicted_data = pd.read_csv('predictions_2023_decision_tree.csv', usecols=['Country', 'January', 'February', 'March', 'April'])

# Merge the actual and predicted DataFrames on the 'Country' column
merged_data = pd.merge(actual_data, predicted_data, on='Country', how='inner', suffixes=('_actual', '_predicted'))

# Arrange the columns in the desired order
cols = ['Country', 'January_actual', 'January_predicted', 'February_actual', 'February_predicted', 'March_actual', 'March_predicted', 'April_actual', 'April_predicted']
merged_data = merged_data[cols]

# Save the merged data to a CSV file
merged_data.to_csv('merged_prediction_vs_actual.csv', index=False)
