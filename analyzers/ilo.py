# Scraper for ilo.org
# Graph Functions
# Author: Ilhan Yavuz Iskurt, Alp Yener, Janset Tunca

# External imports
from pathlib import Path
import pandas as pd
# import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt

# Local imports
from utils.config import config


def inflowGraph(df: pd.DataFrame):
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
    ax.set_ylabel('Migration by thousands')
    ax.set_title('Migration of Working Age Citizens Over Time')

    # Add a legend
    ax.legend()

    # Save the plot as a file (e.g., PNG format)
    plt.savefig(config.GRAPH_DIR / "Inflow.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


def classif2Line(df: pd.DataFrame):
    
    #drop the unnecessary columns
    df = df.drop(["indicator.label", "ref_area.label", "source.label", "obs_status.label",
                 "note_classif.label", "note_indicator.label", "note_source.label"], axis=1)

    # modify the dataframe to reduce the rows of each year
    total_df: pd.DataFrame = df[df["classif2.label"]
                                != "Place of birth: Total"]
    total_df = total_df[total_df["classif2.label"]
                        != "Place of birth: Status unknown"]
    total_df = total_df[total_df["classif1.label"]
                        == "Education (Aggregate levels): Total"]
    total_df = total_df[total_df["sex.label"] == "Sex: Total"]
    
    # drop the columns after being used for modification
    total_df = total_df.drop(["classif1.label", "sex.label"], axis=1)
    
    return total_df




def outsideOfWorkGraph(df: pd.DataFrame):
    
    # seperate df's since the values have a great difference
    df_native: pd.DataFrame = df[df['classif2.label']
                         == 'Place of birth: Native-born']
    df_foreign: pd.DataFrame = df[df['classif2.label']
                          == 'Place of birth: Foreign-born']

    ## FOREIGNER'S PART
    
    df_sorted_f = df_foreign.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_f = df_sorted_f.reset_index(drop=True)

    
    plt.plot(df_sorted_f['time'], df_sorted_f['obs_value'])
    
    plt.xlabel('Years')
    plt.ylabel('Foreigners (in thousands)')
    plt.title('Foreigners outside of labour force by years')

    # Show the plot
    plt.savefig(config.GRAPH_DIR / "OutOfWorkForceForeigners.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()
    
    ## NATIVE'S PART
    
    df_sorted_n = df_native.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_n = df_sorted_n.reset_index(drop=True)

    plt.plot(df_sorted_n['time'], df_sorted_n['obs_value'])
    
    plt.xlabel('Years')
    plt.ylabel('Natives (in thousands)')
    plt.title('Natives outside of labour force by years')

    # Show the plot
    plt.savefig(config.GRAPH_DIR / "OutOfWorkForceNatives.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()


    
def unemployment(df: pd.DataFrame): # basically does the same as the previous function, but for a different purpose
    
    # seperate df's since the values have a great difference
    df_native: pd.DataFrame = df[df['classif2.label']
                         == 'Place of birth: Native-born']
    df_foreign: pd.DataFrame = df[df['classif2.label']
                          == 'Place of birth: Foreign-born']

    ## FOREIGNER'S PART
    
    df_sorted_f = df_foreign.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_f = df_sorted_f.reset_index(drop=True)

    
    plt.plot(df_sorted_f['time'], df_sorted_f['obs_value'])
    
    plt.xlabel('Years')
    plt.ylabel('Foreigners (in thousands)')
    plt.title('Unemployed foreigners by years')

    # Show the plot
    plt.savefig(config.GRAPH_DIR / "UnemployedForeigners.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()
    
    ## NATIVE'S PART
    
    df_sorted_n = df_native.sort_values('time')

    # Reset the index of the sorted DataFrame
    df_sorted_n = df_sorted_n.reset_index(drop=True)

    plt.plot(df_sorted_n['time'], df_sorted_n['obs_value'])
    
    plt.xlabel('Years')
    plt.ylabel('Natives (in thousands)')
    plt.title('Unemployed natives by years')

    # Show the plot
    plt.savefig(config.GRAPH_DIR / "UnemployedNatives.png")

    # Clear plot
    plt.cla()
    plt.clf()
    plt.close()






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
    inflowGraph(sep_dfs[
        "Inflow of working age foreign citizens by sex and country of citizenship (thousands)"])

    # Charts 2 and 3
    outsideOfWorkGraph(classif2Line(sep_dfs["Persons outside the labour force by sex, education and place of birth (in thousands)"]))
    
    # Charts 4 and 5
    unemployment(classif2Line(sep_dfs["Unemployment by sex, education and place of birth (thousands)"]))
