import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from src.enums import QCol, Strat

def visualisation2(df: pd.DataFrame):
    w_df = df[
        (df['YEAR'] == 2024) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][['WALKABILITY_INDEX', QCol.OBESITY_18_PLUS.value, QCol.OVERWEIGHT_18_PLUS.value]]

    # https://www.statology.org/pandas-scatter-plot-multiple-columns/
    ax = w_df.plot(kind="scatter", 
        x="WALKABILITY_INDEX",
        y=QCol.OBESITY_18_PLUS.value, 
        color="red", 
        label="Obese",
        s=40,
        alpha=0.7
    )

    w_df.plot(kind="scatter", 
        x="WALKABILITY_INDEX", 
        y=QCol.OVERWEIGHT_18_PLUS.value, 
        color="purple", 
        label="Overweight", 
        s=40,
        alpha=0.7,
        ax=ax
    )

    # Correlation lines
    # https://www.geeksforgeeks.org/data-visualization/how-to-draw-a-line-inside-a-scatter-plot/
    w_df.dropna(inplace=True) # Otherwise we get an errror
    x = w_df['WALKABILITY_INDEX']

    # Obese
    y = w_df[QCol.OBESITY_18_PLUS.value]

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
    y = w_df[QCol.OVERWEIGHT_18_PLUS.value]

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

if __name__ == "__main__":
    from src.lib.db import load_df_from_db
    
    visualisation2(load_df_from_db())