import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from enums import Region, QuestionID, StratID
from utils import ensure_dir
from lib.db import load_df_from_db

# https://matplotlib.org/stable/gallery/color/named_colors.html

matplotlib.use('tkagg')
# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
plt.style.use("seaborn-v0_8")

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
    plt.ylabel("Adult Population (%)")

    plt.tight_layout()

    # Save to file
    plt.savefig('./figures/figure1.png')

    plt.show()

def visualisation2():
    df_obese = filter_stats_year(2024, StratID.OVERALL, QuestionID.OBESITY_18_PLUS)
    df_overweight = filter_stats_year(2024, StratID.OVERALL, QuestionID.OVERWEIGHT_18_PLUS)

    # https://www.statology.org/pandas-scatter-plot-multiple-columns/
    ax = df_obese.plot(kind="scatter", 
        x="Walkability_Index",
        y="Data_Value", 
        color="red", 
        label="Obese %",
        s=40,
        alpha=0.7
    )

    df_overweight.plot(kind="scatter", 
        x="Walkability_Index", 
        y="Data_Value", 
        color="purple", 
        label="Overweight %", 
        s=40,
        alpha=0.7,
        ax=ax
    )

    # Correlation lines
    # https://www.geeksforgeeks.org/data-visualization/how-to-draw-a-line-inside-a-scatter-plot/

    # Obese
    df_obese.dropna(inplace=True) # Otherwise we get an errror

    x = df_obese['Walkability_Index']
    y = df_obese['Data_Value']

    slope, intercept = np.polyfit(x, y, 1)
    line = slope * x + intercept

    ax.plot(
        x, 
        line, 
        linestyle='-',
        color="tab:red",
        alpha=0.9
    )

    
    # Overweight
    df_overweight.dropna(inplace=True) # Otherwise we get an errror

    x = df_overweight['Walkability_Index']
    y = df_overweight['Data_Value']

    slope, intercept = np.polyfit(x, y, 1)
    line = slope * x + intercept

    ax.plot(
        x, 
        line, 
        linestyle='-',
        color="tab:purple",
        alpha=0.9
    )

    ax.set_xlabel("Walkability Index")
    ax.set_ylabel("Adult Population (%)")
    ax.set_title("Walkability vs. Adult Population Weight Category")

    plt.tight_layout()

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