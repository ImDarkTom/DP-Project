import matplotlib.pyplot as plt

from . import df

from src.enums import QCol, Strat
from src.utils import plot_correlation


def visualisation2():
    w_df = df[
        (df['YEAR'] == 2024) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][['WALKABILITY_INDEX', QCol.OBESITY_18_PLUS.value, QCol.OVERWEIGHT_18_PLUS.value]]

    # https://www.statology.org/pandas-scatter-plot-multiple-columns/
    ax = w_df.plot(kind="scatter", 
        x="WALKABILITY_INDEX",
        y=QCol.OBESITY_18_PLUS.value, 
        color="tab:red", 
        label="Obese",
    )

    w_df.plot(kind="scatter", 
        x="WALKABILITY_INDEX", 
        y=QCol.OVERWEIGHT_18_PLUS.value, 
        color="tab:purple", 
        label="Overweight", 
        ax=ax
    )

    # Correlation lines
    # https://www.geeksforgeeks.org/data-visualization/how-to-draw-a-line-inside-a-scatter-plot/
    w_df.dropna(inplace=True)

    x = w_df['WALKABILITY_INDEX']

    plot_correlation(x, w_df[QCol.OBESITY_18_PLUS.value], ax, "tab:red")
    plot_correlation(x, w_df[QCol.OVERWEIGHT_18_PLUS.value], ax, "tab:purple")

    ax.set_xlabel("Walkability Index")
    ax.set_ylabel("Adult Population (%)")
    ax.set_title("Walkability vs. Adult Population Weight Category")

    plt.tight_layout()

    plt.savefig('./figures/fig2_walkability_vs_weight.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    visualisation2()