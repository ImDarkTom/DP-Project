import matplotlib.pyplot as plt

from . import df

from src.enums import QCol, Strat
from src.utils import plot_correlation


def visualisation3():
    # After exploration 2023 is the latest date that has exercise data
    df2 = df[
        (df['YEAR'] == 2023) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][[
        'YEAR', 
        'LOCATION',
        QCol.WALKABILITY_INDEX.value,
        QCol.MOD_AEROBIC_150_MIN.value,
        QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value,
        QCol.MOD_AEROBIC_300_MIN.value,
        QCol.MUSCLE_2_DAYS.value
    ]]

    df2.dropna(inplace=True)

    fig, axs = plt.subplots(2, 2)

    df2.plot.scatter(
        x=QCol.WALKABILITY_INDEX.value,
        y=QCol.MOD_AEROBIC_150_MIN.value,
        ax=axs[0][0],
        color="tab:blue",
    )


    df2.plot.scatter(
        x=QCol.WALKABILITY_INDEX.value,
        y=QCol.MOD_AEROBIC_300_MIN.value,
        ax=axs[0][1],
        color="tab:green"
    )

    df2.plot.scatter(
        x=QCol.WALKABILITY_INDEX.value,
        y=QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value,
        ax=axs[1][0],
        color="tab:purple"
    )

    df2.plot.scatter(
        x=QCol.WALKABILITY_INDEX.value,
        y=QCol.MUSCLE_2_DAYS.value,
        ax=axs[1][1],
        color="tab:red",
    )

    axs[0][0].set_xlabel("Walkability Index")
    axs[1][0].set_xlabel("Walkability Index")
    axs[0][1].set_xlabel("Walkability Index")
    axs[1][1].set_xlabel("Walkability Index")

    axs[0][0].set_ylabel("Adult Population (%)")
    axs[1][0].set_ylabel("Adult Population (%)")
    axs[0][1].set_ylabel("Adult Population (%)")
    axs[1][1].set_ylabel("Adult Population (%)")

    fig.tight_layout()

    fig.legend([
        '≥150 min Aerobic Activity (%)',
        '≥150 min Aerobic + Muscle 2x/wk (%)',
        '≥300 min Aerobic Activity (%)',
        'Muscle Strengthening ≥ 2x/wk (%)'
    ], loc='upper right', bbox_to_anchor=(1, 0.94))

    fig.suptitle("Weekly Exercise vs. Walkability")
    fig.subplots_adjust(top=0.72)

    plot_correlation(
        df2[QCol.WALKABILITY_INDEX.value],
        df2[QCol.MOD_AEROBIC_150_MIN.value],
        axs[0][0],
        "tab:blue"
    )

    plot_correlation(
        df2[QCol.WALKABILITY_INDEX.value],
        df2[QCol.MOD_AEROBIC_300_MIN.value],
        axs[0][1],
        "tab:green"
    )

    plot_correlation(
        df2[QCol.WALKABILITY_INDEX.value],
        df2[QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value],
        axs[1][0],
        "tab:purple"
    )

    plot_correlation(
        df2[QCol.WALKABILITY_INDEX.value],
        df2[QCol.MUSCLE_2_DAYS.value],
        axs[1][1],
        "tab:red"
    )

    plt.savefig('./figures/fig3_exercise_vs_walkability.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    visualisation3()
