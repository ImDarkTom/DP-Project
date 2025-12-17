import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from enums import Region, QCol, Strat
from utils import ensure_dir
from lib.db import load_df_from_db

# https://matplotlib.org/stable/gallery/color/named_colors.html

matplotlib.use('tkagg')
# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
plt.style.use("seaborn-v0_8")

df = load_df_from_db("merged_dataset")

def filter_stats(
    region: Region,
    stratID: Strat,
    questionID: QCol,
):
    return df \
        .loc[df['LOCATION'] == region.value] \
        .loc[df['STRATIFICATION'] == stratID.value] \
        .loc[df['QuestionID'] == questionID.value] \
        .convert_dtypes()

def filter_stats_year(
    year: int,
    stratID: Strat,
    questionID: QCol,
):
    return df \
        .loc[df['Year'] == year] \
        .loc[df['StratificationID1'] == stratID.value] \
        .loc[df['QuestionID'] == questionID.value] \
        .convert_dtypes()

def visualisation1():
    # Get year, values for obesity and overweight percentages, where location is all and strat is overall
    w_df = df[
        (df['LOCATION'] == Region.ALL.value) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][['YEAR', QCol.OBESITY_18_PLUS.value, QCol.OVERWEIGHT_18_PLUS.value]]

    ax = w_df.plot(
        x="YEAR", 
        y=QCol.OBESITY_18_PLUS.value,
        color="tab:red",
        label="% Obese",
    )

    w_df.plot(
        x="YEAR",
        y=QCol.OVERWEIGHT_18_PLUS.value,
        color="tab:purple",
        label="% Overweight",
        ax=ax,
    )

    plt.title("% of adults over 18 that have obesity")
    plt.xlabel("Year")
    plt.ylabel("Adult Population (%)")

    plt.tight_layout()

    # Save to file
    plt.savefig('./figures/figure1.png')

    plt.show()

# def visualisation2():
#     df_obese = filter_stats_year(2024, StratID.OVERALL, QuestionID.OBESITY_18_PLUS)
#     df_overweight = filter_stats_year(2024, StratID.OVERALL, QuestionID.OVERWEIGHT_18_PLUS)

#     # https://www.statology.org/pandas-scatter-plot-multiple-columns/
#     ax = df_obese.plot(kind="scatter", 
#         x="Walkability_Index",
#         y="Data_Value", 
#         color="red", 
#         label="Obese %",
#         s=40,
#         alpha=0.7
#     )

#     df_overweight.plot(kind="scatter", 
#         x="Walkability_Index", 
#         y="Data_Value", 
#         color="purple", 
#         label="Overweight %", 
#         s=40,
#         alpha=0.7,
#         ax=ax
#     )

#     # Correlation lines
#     # https://www.geeksforgeeks.org/data-visualization/how-to-draw-a-line-inside-a-scatter-plot/

#     # Obese
#     df_obese.dropna(inplace=True) # Otherwise we get an errror

#     x = df_obese['Walkability_Index']
#     y = df_obese['Data_Value']

#     slope, intercept = np.polyfit(x, y, 1)
#     line = slope * x + intercept

#     ax.plot(
#         x, 
#         line, 
#         linestyle='-',
#         color="tab:red",
#         alpha=0.9
#     )

    
#     # Overweight
#     df_overweight.dropna(inplace=True) # Otherwise we get an errror

#     x = df_overweight['Walkability_Index']
#     y = df_overweight['Data_Value']

#     slope, intercept = np.polyfit(x, y, 1)
#     line = slope * x + intercept

#     ax.plot(
#         x, 
#         line, 
#         linestyle='-',
#         color="tab:purple",
#         alpha=0.9
#     )

#     ax.set_xlabel("Walkability Index")
#     ax.set_ylabel("Adult Population (%)")
#     ax.set_title("Walkability vs. Adult Population Weight Category")

#     plt.tight_layout()

#     plt.savefig('./figures/figure2.png')

#     plt.show()

# def visualisation3():
#     df_ov = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.OVERWEIGHT_18_PLUS)
#     df_ob = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.OBESITY_18_PLUS)

#     df_veg = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.VEG_LT_ONCE_DAILY)
#     df_fru = filter_stats(Region.ALL, StratID.OVERALL, QuestionID.FRUIT_LT_ONCE_DAILY)

#     df_ov = df_ov[['Data_Value', 'Year']].rename(columns={'Data_Value': 'Overweight_Percent'})
#     df_ob = df_ob[['Data_Value', 'Year']].rename(columns={'Data_Value': 'Obese_Percent'})
#     df_veg = df_veg[['Data_Value', 'Year']].rename(columns={'Data_Value': 'Veg_LT_Daily_Percent'})
#     df_fru = df_fru[['Data_Value', 'Year']].rename(columns={'Data_Value': 'Fruit_LT_Daily_Percent'})

#     df2 = (
#         df_ov
#             .merge(df_ob, on='Year')
#             .merge(df_veg, on='Year')
#             .merge(df_fru, on='Year')
#     )

#     # Plot individually so we can customise the line styles

#     ax = df2.plot(
#         x="Year", 
#         y="Obese_Percent", 
#         color="tab:red",
#         linestyle="-",
#         label="% obese"
#     )

#     df2.plot(
#         x="Year", 
#         y="Overweight_Percent", 
#         color="tab:purple",
#         linestyle="-",
#         ax=ax,
#         label="% overweight"
#     )

#     df2.plot(
#         x="Year", 
#         y="Veg_LT_Daily_Percent", 
#         color="tab:green",
#         linestyle=":",
#         ax=ax,
#         label="% eating vegetables less than daily"
#     )

#     df2.plot(
#         x="Year", 
#         y="Fruit_LT_Daily_Percent", 
#         color="tab:blue",
#         linestyle=":",
#         ax=ax,
#         label="% eating fruit less than daily"
#     )

#     plt.title("Diet vs. Weight Class")
#     plt.xlabel("Year")
#     plt.ylabel("Adult Population (%)")

#     plt.tight_layout()

#     # Save to file
#     plt.savefig('./figures/figure3.png')

#     plt.show()

# def visualisation4():
#     df_ae15 = filter_stats_year(2024, StratID.OVERALL, QuestionID.MOD_AEROBIC_150_MIN)
#     df_ae30 = filter_stats_year(2024, StratID.OVERALL, QuestionID.MOD_AEROBIC_300_MIN)

#     df_ae15 = df_ae15[['Data_Value', 'LocationAbbr']].rename(columns={'Data_Value': 'Mod_Aerobic_150_Min'})
#     df_ae30 = df_ae30[['Data_Value', 'LocationAbbr']].rename(columns={'Data_Value': 'Mod_Aerobic_300_Min'})

#     print(df_ae15, df_ae30)

#     df2 = (
#         df_ae15
#             .merge(df_ae30, on='LocationAbbr')
#     )
    
#     print(df2)

#     return
#     # Plot individually so we can customise the line styles

#     ax = df2.plot(
#         x="Year", 
#         y="Obese_Percent", 
#         color="tab:red",
#         linestyle="-",
#         label="% obese"
#     )

#     df2.plot(
#         x="Year", 
#         y="Overweight_Percent", 
#         color="tab:purple",
#         linestyle="-",
#         ax=ax,
#         label="% overweight"
#     )

#     df2.plot(
#         x="Year", 
#         y="Veg_LT_Daily_Percent", 
#         color="tab:green",
#         linestyle=":",
#         ax=ax,
#         label="% eating vegetables less than daily"
#     )

#     df2.plot(
#         x="Year", 
#         y="Fruit_LT_Daily_Percent", 
#         color="tab:blue",
#         linestyle=":",
#         ax=ax,
#         label="% eating fruit less than daily"
#     )

#     plt.title("Diet vs. Weight Class")
#     plt.xlabel("Year")
#     plt.ylabel("Adult Population (%)")

#     plt.tight_layout()

#     # Save to file
#     plt.savefig('./figures/figure3.png')

#     plt.show()

def visualise_data():
    ensure_dir('./figures/')
    # Obesity and overweight change over time
    visualisation1()

    # # weight class vs state avg walkability index
    # visualisation2()

    # # diet vs weight class
    # visualisation3()

    # exercise vs walkability
    # visualisation4()


    # todo: 
    # - exercise vs walkability
    # - exercise vs weight class
    # - diet vs income


if __name__ == "__main__":
    visualise_data()