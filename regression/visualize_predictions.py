import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV files
df_actual = pd.read_csv("melted.csv")
df_2023 = pd.read_csv("melted_predicted_2023.csv")

# Convert 'Year' and 'Month' columns to datetime format
df_actual['Date'] = pd.to_datetime(df_actual['Year'].astype(str) + '-' + df_actual['Month'].astype(str), format='%Y-%B')
df_2023['Date'] = pd.to_datetime(df_2023['Year'].astype(str) + '-' + df_2023['Month'].astype(str), format='%Y-%m')

# Drop 'Year' and 'Month' columns from df_2023
df_2023 = df_2023.drop(['Year', 'Month'], axis=1)

# Get the unique countries from df_2023
countries_df2 = df_2023['Country'].unique()

# Filter df_actual based on countries in df_2023
filtered_df1 = df_actual[df_actual['Country'].isin(countries_df2)]

# Merge df_actual and df_2023
merged_df = pd.concat([filtered_df1, df_2023])
merged_df.to_csv("out.csv")

# Sort the dataframe by country and date
merged_df = merged_df.sort_values(['Country', 'Date']).reset_index(drop=True)

# Plot a line for each country
plt.figure(figsize=(12, 8))

for country, group in merged_df.groupby('Country'):
    plt.plot(group['Date'], group['Sales'], label=country)

plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Property sales by year and month by Country')
plt.legend()
plt.axvline(pd.to_datetime('2023'), color='r', linestyle='--', label='2023')
plt.xticks(rotation=45)
plt.show()
