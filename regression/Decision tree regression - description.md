Decision tree regression - description
Steps:
1)Loaded raw dataset from https://www.imtilak.net/en/turkey/news/realestate-sales-statistics-turkey-2022
2)Manually transformed(the file looked like a pdf before that), save to file "property_raw_table.csv"
3)Run preprocess_propert_data.py
4)Run property_data_decision_tree_regressor.py
5)Run comparison.py
6)Obtain files:    
    - merged_prediction_vs_actual.csv // comparison of the actual data for the first 4 months of 2023 with predicted data from the model

    -predictions_2023_decision_tree.csv // the result of the regression model, shows estimates for property sales in Turkiye the year 2023 to nationals of each country by month
