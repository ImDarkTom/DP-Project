import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from src.enums import QCol, Strat, Region

def visualisation5(df: pd.DataFrame):
    # After exploration 2021 is the latest date that has fruit/veg data
    df2 = df[
        (df['LOCATION'] == Region.ALL.value) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][[
        'YEAR',
        QCol.OBESITY_18_PLUS.value,
        QCol.OVERWEIGHT_18_PLUS.value,
    ]]

    df2.dropna(inplace=True)

    x = df2['YEAR'].to_frame()
    y = df2[QCol.OBESITY_18_PLUS.value].to_frame()

    model = LinearRegression()
    model.fit(x, y)

    future_years = pd.DataFrame({
        "YEAR": range(df['YEAR'].min(), df['YEAR'].max() + 7)
    })

    future_years["PREDICTED_OBESITY"] = model.predict(future_years)

    prediction = pd.concat([df2, future_years], ignore_index=True)

    ax = prediction.plot(
        x='YEAR',
        y=QCol.OBESITY_18_PLUS.value,
        color="tab:blue",
        label="Observed Obese Population (%)"
    )

    prediction.plot(
        x='YEAR',
        y='PREDICTED_OBESITY',
        color="tab:cyan",
        linestyle='--',
        alpha=0.5,
        ax=ax,
        label="Predicted Obese Population (%)"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Adult Population (%)")

    plt.tight_layout()
    plt.subplots_adjust(top=0.92) # otherwise title clips

    plt.suptitle("Weight Class Model Prediction")

    plt.savefig('./figures/fig5_weight_class_model.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    from src.lib.db import load_df_from_db

    visualisation5(load_df_from_db())
