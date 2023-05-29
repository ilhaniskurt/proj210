# Scraper for ilo.org
# Author: Ilhan Yavuz Iskurt, Alp Yener

# External imports
from pathlib import Path
import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

# Local imports
from utils.config import config


def analyze():
    # Read csv
    datapath = Path(config.DATA_DIR)
    file = list(datapath.glob(config.ILO_DATA + "*"))
    df = pd.read_csv(file[0])

    label_column = 'indicator.label'

    # Get unique labels from the label column
    labels = df[label_column].unique()

    # Create separate DataFrames for each label
    sep_dfs = {
        label: df[df[label_column] == label] for label in labels}

    # Chart 1
    df1 = sep_dfs[
        "Inflow of working age foreign citizens by sex and country of citizenship (thousands)"]
    print(df1.iloc[1:6].columns)
    print(df1["time"].head())
    # for k in sep_dfs.keys():
    #     print(k)
