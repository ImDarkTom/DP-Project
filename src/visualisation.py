import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from enums import Region, QuestionID, StratID
from utils import ensure_dir
from lib.db import load_df_from_db

matplotlib.use('tkagg')

df = load_df_from_db("merged_dataset")

def filter_stats(
    region: Region,
    stratID: StratID,
    questionID: QuestionID,
):
    return df \
        .loc[df['LocationAbbr'] == region.value] \
        .loc[df['StratificationID1'] == stratID.value] \
        .loc[df['QuestionID'] == questionID.value] \
        .convert_dtypes()

def filter_stats_year(
    year: int,
    stratID: StratID,
    questionID: QuestionID,
):
    return df \
        .loc[df['Year'] == year] \
        .loc[df['StratificationID1'] == stratID.value] \
        .loc[df['QuestionID'] == questionID.value] \
        .convert_dtypes()

def visualisation1():
    obesity_df = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.OBESITY_18_PLUS)
    overweight_df = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.OVERWEIGHT_18_PLUS)

    # Rename cols so when we merge them they don't collide
    obesity_df.rename(columns={ 'Data_Value': 'Percent_Obese' }, inplace=True)
    overweight_df.rename(columns={ 'Data_Value': 'Percent_Overweight' }, inplace=True)

    merged_df = pd.merge(obesity_df, overweight_df, on='Year')

    merged_df.plot(
        x="Year", 
        y=["Percent_Obese", "Percent_Overweight"], 
        style={
            "Percent_Obese": "r--",
            "Percent_Overweight": "b:"
        },
    )

    plt.title("% of adults over 18 that have obesity")
    plt.xlabel("Year")
    plt.ylabel("% of population ")

    # Save to file
    plt.savefig('./figures/figure1.png')

    plt.show()

def visualisation2():
    res = filter_stats_year(2024, StratID.OVERALL, QuestionID.OBESITY_18_PLUS)

    res.rename(columns={ 'Data_Value': 'Percent_Obese' }, inplace=True)
    
    res.plot.scatter(
        x="Walkability_Index", 
        y="Percent_Obese",
        c="Percent_Obese",
    )

    plt.title("State Walkability Index vs % of State population in 'Obese' weight class")
    # plt.xlabel("Year")
    # plt.ylabel("% of population ")

    # Save to file
    plt.savefig('./figures/figure2.png')

    plt.show()

def visualise_data():
    ensure_dir('./figures/')
    # Obesity and overweight change over time
    visualisation1()

    # Scatter plot
    visualisation2()

if __name__ == "__main__":
    visualise_data()