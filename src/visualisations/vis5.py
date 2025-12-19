import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from . import df

from src.enums import QCol, Strat, Region


def visualisation5(
    stratification: Strat = Strat.OVERALL, 
    filename: str = 'fig5_weight_class_model',
    title_suffix: str = 'Overall',
    label: str = 'Adult Population (%)'
):
    # After exploration 2021 is the latest date that has fruit/veg data
    df2 = df[
        (df['LOCATION'] == Region.ALL.value) &
        (df['STRATIFICATION'] == stratification.value)
    ][[
        'YEAR',
        QCol.OBESITY_18_PLUS.value,
        QCol.OVERWEIGHT_18_PLUS.value,
    ]]

    df2.dropna(inplace=True)

    x_years = df2['YEAR'].to_frame()

    # Predict Obesity
    y_obesity = df2[QCol.OBESITY_18_PLUS.value].to_frame()

    obesity_model = LinearRegression()
    obesity_model.fit(x_years, y_obesity)

    future_years = pd.DataFrame({
        "YEAR": range(df2['YEAR'].min(), df2['YEAR'].max() + 7)
    })

    future_years["PREDICTED_OBESITY"] = obesity_model.predict(future_years)

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

    # Predict Overweight
    y_overweight = df2[QCol.OVERWEIGHT_18_PLUS.value].to_frame()

    overweight_model = LinearRegression()
    overweight_model.fit(x_years, y_overweight)

    future_years["PREDICTED_OVERWEIGHT"] = overweight_model.predict(future_years['YEAR'].to_frame())

    prediction = pd.concat([prediction, future_years], ignore_index=True)

    prediction.plot(
        x='YEAR',
        y=QCol.OVERWEIGHT_18_PLUS.value,
        color="tab:purple",
        label="Observed Owerweight Population (%)",
        ax=ax
    )

    prediction.plot(
        x='YEAR',
        y='PREDICTED_OVERWEIGHT',
        color="tab:pink",
        linestyle='--',
        alpha=0.5,
        ax=ax,
        label="Predicted Overweight Population (%)"
    )

    ax.set_xlabel("Year")
    ax.set_ylabel(label)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92) # otherwise title clips

    plt.suptitle("Weight Class Model Prediction - " + title_suffix)

    plt.savefig(f'./figures/{filename}.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    visualisation5()
