import matplotlib.pyplot as plt
import pandas as pd

from src.enums import Region, QCol, Strat

def visualisation1(df: pd.DataFrame):
    # Get year, values for obesity and overweight percentages, where location is all and strat is overall
    w_df = df[
        (df['LOCATION'] == Region.ALL.value) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][['YEAR', QCol.OBESITY_18_PLUS.value, QCol.OVERWEIGHT_18_PLUS.value]]

    ax = w_df.plot(
        x="YEAR", 
        y=QCol.OBESITY_18_PLUS.value,
        color="tab:red",
        label="Obese",
    )

    w_df.plot(
        x="YEAR",
        y=QCol.OVERWEIGHT_18_PLUS.value,
        color="tab:purple",
        label="Overweight",
        ax=ax,
    )

    plt.title("Weight Class of U.S. Adults")
    plt.xlabel("Year")
    plt.ylabel("Adult Population (%)")

    plt.tight_layout()

    # Save to file
    plt.savefig('./figures/fig1_weight_class.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    from src.lib.db import load_df_from_db
    
    visualisation1(load_df_from_db())