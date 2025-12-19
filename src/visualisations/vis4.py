import matplotlib.pyplot as plt

from . import df

from src.enums import QCol, Strat
from src.utils import plot_correlation


def visualisation4():
    # After exploration 2021 is the latest date that has fruit/veg data
    df2 = df[
        (df['YEAR'] == 2021) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][[
        'LOCATION',
        QCol.OBESITY_18_PLUS.value,
        QCol.OVERWEIGHT_18_PLUS.value,
        QCol.VEG_LT_ONCE_DAILY.value,
        QCol.FRUIT_LT_ONCE_DAILY.value,
    ]]

    df2.dropna(inplace=True)

    fig, axs = plt.subplots(2, 2)

    df2.plot.scatter(
        x=QCol.OBESITY_18_PLUS.value,
        y=QCol.FRUIT_LT_ONCE_DAILY.value,
        ax=axs[0][0],
        color="tab:blue",
    )


    df2.plot.scatter(
        x=QCol.OBESITY_18_PLUS.value,
        y=QCol.VEG_LT_ONCE_DAILY.value,
        ax=axs[0][1],
        color="tab:green"
    )

    df2.plot.scatter(
        x=QCol.OVERWEIGHT_18_PLUS.value,
        y=QCol.FRUIT_LT_ONCE_DAILY.value,
        ax=axs[1][0],
        color="tab:purple"
    )

    df2.plot.scatter(
        x=QCol.OVERWEIGHT_18_PLUS.value,
        y=QCol.VEG_LT_ONCE_DAILY.value,
        ax=axs[1][1],
        color="tab:red",
    )

    axs[0][0].set_xlabel("Obese Population (%)")
    axs[1][0].set_xlabel("Obese Population (%)")
    axs[0][1].set_xlabel("Overweight Population (%)")
    axs[1][1].set_xlabel("Overweight Population (%)")

    axs[0][0].set_ylabel("Eats Fruit LT Daily (%)")
    axs[1][0].set_ylabel("Eats Veg. LT Daily (%)")
    axs[0][1].set_ylabel("Eats Fruit LT Daily (%)")
    axs[1][1].set_ylabel("Eats Veg. LT Daily (%)")

    fig.tight_layout()

    fig.legend([
        'Obese, Fruit ≥Daily (%)',
        'Obese, Vegetables ≥Daily (%)',
        'Overweight, Fruit ≥Daily (%)',
        'Overweight, Vegetables >Daily (%)'
    ], loc='upper right', bbox_to_anchor=(1, 0.94))

    fig.suptitle("Diet. vs. Weight Class")
    fig.subplots_adjust(top=0.72)

    plot_correlation(
        df2[QCol.OBESITY_18_PLUS.value],
        df2[QCol.FRUIT_LT_ONCE_DAILY.value],
        axs[0][0],
        "tab:blue"
    )

    plot_correlation(
        df2[QCol.OBESITY_18_PLUS.value],
        df2[QCol.VEG_LT_ONCE_DAILY.value],
        axs[0][1],
        "tab:green"
    )

    plot_correlation(
        df2[QCol.OVERWEIGHT_18_PLUS.value],
        df2[QCol.FRUIT_LT_ONCE_DAILY.value],
        axs[1][0],
        "tab:purple"
    )

    plot_correlation(
        df2[QCol.OVERWEIGHT_18_PLUS.value],
        df2[QCol.VEG_LT_ONCE_DAILY.value],
        axs[1][1],
        "tab:red"
    )

    plt.savefig('./figures/fig4_diet_vs_weight.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    visualisation4()
