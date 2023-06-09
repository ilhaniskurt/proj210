# Scraper for ilo.org
# Author: Ilhan Yavuz Iskurt, Alp Yener

# External imports
from pathlib import Path
import pandas as pd
# import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt

# Local imports
from utils.config import config


def graph1(df: pd.DataFrame):
    df = df.drop("indicator.label", axis=1)
    total_df: pd.DataFrame = df[df["sex.label"] == "Sex: Total"]

    df_sum = total_df.groupby('classif1.label')[
        'obs_value'].sum().reset_index()
    top_labels = df_sum.nlargest(6, 'obs_value')['classif1.label']
    df_top = total_df[total_df['classif1.label'].isin(top_labels)]

    fig, ax = plt.subplots(figsize=(10, 6))
    for label, group in df_top.groupby("classif1.label"):
        label = label.replace("Country of citizenship: ", "")

        # Sort the group by time values
        group = group.sort_values("time")

        ax.plot(group["time"], group["obs_value"], label=label)

    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Migration by thousand')
    ax.set_title('Migration over Time')

    # Add a legend
    ax.legend()

    # Save the plot as a file (e.g., PNG format)
    plt.savefig(config.GRAPH_DIR / "graph1.png")


def graph2(df: pd.DataFrame):
    df = df.drop("indicator.label", axis=1)

    df = df.drop(["ref_area.label", "source.label", "obs_status.label",
                 "note_classif.label", "note_indicator.label", "note_source.label"], axis=1)

    total_df: pd.DataFrame = df[df["classif2.label"]
                                != "Place of birth: Total"]
    total_df = total_df[total_df["classif2.label"]
                        != "Place of birth: Status unknown"]
    total_df = total_df[total_df["classif1.label"]
                        == "Education (Aggregate levels): Total"]
    total_df = total_df[total_df["sex.label"] == "Sex: Total"]

    total_df = total_df.drop(["classif1.label", "sex.label"], axis=1)

    df_native = total_df[total_df['classif2.label']
                         == 'Place of birth: Native-born']
    df_foreign = total_df[total_df['classif2.label']
                          == 'Place of birth: Foreign-born']

    df_sorted = df_foreign.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted = df_sorted.reset_index(drop=True)

    plt.plot(df_sorted['time'], df_sorted['obs_value'], label='Foreign')

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Line Graph')
    plt.legend()

    # Show the plot
    plt.savefig(config.GRAPH_DIR / "graph2.png")


def analyze():
    # Read csv
    datapath = Path(config.DATA_DIR)
    file = list(datapath.glob(config.ILO_DATA + "*"))
    df = pd.read_csv(file[0])

    label_column = 'indicator.label'

    # Drop irrelevant columns from DataFrame
    # df = df.drop(["ref_area.label", "source.label", "classif2.label", "obs_status.label",
    # "note_classif.label", "note_indicator.label", "note_source.label"], axis=1)

    # Get unique labels from the label column
    labels = df[label_column].unique()

    # Create separate DataFrames for each label
    sep_dfs = {
        label: df[df[label_column] == label] for label in labels}

    # Chart 1
    graph1(sep_dfs[
        "Inflow of working age foreign citizens by sex and country of citizenship (thousands)"])

    # Chart 2
    graph2(
        sep_dfs["Persons outside the labour force by sex, education and place of birth (in thousands)"])
