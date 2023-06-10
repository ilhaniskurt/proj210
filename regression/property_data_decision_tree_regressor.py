import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
import calendar

# Load the dataset
data = pd.read_csv('data_without_2023.csv')

# Split column titles and keep only the first part, capitalized
data.columns = data.columns.str.split(' ').str[0].str.capitalize()

# Extract the part before the hyphen "-" in the "Country" column
data['Country'] = data['Country'].str.split('-').str[0]

# Preprocess the data - Remove spaces from all columns
data = data.replace(' ', '', regex=True)

# Extract the relevant columns
months = data.columns[2:]  # Assuming the months start from the third column

# Create an empty DataFrame for melted data
melted_data = pd.DataFrame(columns=['Year', 'Country', 'Month', 'Sales'])

# Iterate over each row in the original data
for index, row in data.iterrows():
    year = row['Year']
    country = row['Country']
    for month in months:
        # Extract the month value
        month_value = row[month]
        # Create a new row with the month value in the "Sales" column
        new_row = pd.Series([year, country, month, month_value], index=melted_data.columns)
        # Append the new row to the melted data DataFrame
        melted_data = melted_data.append(new_row, ignore_index=True)

# Prepare the feature matrix X_train for training
X_train = melted_data[['Year', 'Country', 'Month']].copy()

# Perform one-hot encoding for the 'Country' and 'Month' columns
encoder = OneHotEncoder(sparse=False)
encoded_features = encoder.fit_transform(X_train[['Country', 'Month']])
encoded_columns = encoder.get_feature_names_out(['Country', 'Month'])
encoded_df = pd.DataFrame(encoded_features, columns=encoded_columns)

# Concatenate the encoded features with the original 'Year' column
X_train_encoded = pd.concat([X_train['Year'], encoded_df], axis=1)

# Prepare the target variable y_train for training
y_train = melted_data['Sales']

# Fit the decision tree regressor
model = DecisionTreeRegressor()
model.fit(X_train_encoded, y_train)

# Prepare the feature matrix X_test for prediction (year 2023, month names for all countries)
countries = data['Country'].unique()
months_2023 = list(calendar.month_name)[1:13]  # Get month names from January to December
X_test = pd.DataFrame({'Year': np.full(len(countries) * len(months_2023), 2023),
                       'Country': np.repeat(countries, len(months_2023)),
                       'Month': np.tile(months_2023, len(countries))})

# Perform one-hot encoding for the 'Country' and 'Month' columns in the test data
encoded_features_test = encoder.transform(X_test[['Country', 'Month']])
encoded_df_test = pd.DataFrame(encoded_features_test, columns=encoded_columns)

# Concatenate the encoded features with the original 'Year' column in the test data
X_test_encoded = pd.concat([X_test['Year'], encoded_df_test], axis=1)

# Predict the 2023 values for each country
predictions = model.predict(X_test_encoded)

# Reshape predictions to match the shape of the months and countries
predictions_reshaped = predictions.reshape(len(countries), len(months))

# Store the predictions in the DataFrame
predictions_2023 = pd.DataFrame(predictions_reshaped, index=data['Country'].unique(), columns=months)

# Export the predictions to a CSV file
predictions_2023.to_csv('predictions_2023_decision_tree.csv', index_label='Country')
