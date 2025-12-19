import matplotlib.pyplot as plt

from . import df

from src.enums import QCol, Strat
from src.utils import plot_correlation


def visualisation6():
    # After exploration 2023 is the latest date that has exercise data
    df2 = df[
        (df['YEAR'] == 2023) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][[
        QCol.OVERWEIGHT_18_PLUS.value,
        QCol.OBESITY_18_PLUS.value,
        QCol.MOD_AEROBIC_150_MIN.value,
        QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value,
        QCol.MOD_AEROBIC_300_MIN.value,
        QCol.MUSCLE_2_DAYS.value
    ]]

    df2['AVG_EXERCISE_AEROBIC'] = df2[[
        QCol.MOD_AEROBIC_150_MIN.value,
        QCol.MOD_AEROBIC_300_MIN.value,
        QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value
    ]].mean(axis="columns")

    df2['AVG_EXERCISE_MUSCLE'] = df2[[
        QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value,
        QCol.MUSCLE_2_DAYS.value
    ]].mean(axis="columns")

    df2.dropna(inplace=True)

    fig, axs = plt.subplots(2, 2)

    df2.plot.scatter(
        x=QCol.OBESITY_18_PLUS.value,
        y='AVG_EXERCISE_AEROBIC',
        ax=axs[0][0],
        color="tab:blue",
    )

    df2.plot.scatter(
        x=QCol.OBESITY_18_PLUS.value,
        y='AVG_EXERCISE_MUSCLE',
        ax=axs[1][0],
        color="tab:orange",
    )

    df2.plot.scatter(
        x=QCol.OVERWEIGHT_18_PLUS.value,
        y='AVG_EXERCISE_AEROBIC',
        ax=axs[0][1],
        color="tab:green",
    )

    df2.plot.scatter(
        x=QCol.OVERWEIGHT_18_PLUS.value,
        y='AVG_EXERCISE_MUSCLE',
        ax=axs[1][1],
        color="tab:red",
    )

    axs[0][0].set_xlabel("Obese Adult Population (%)")
    axs[1][0].set_xlabel("Obese Adult Population (%)")
    axs[0][1].set_xlabel("Overweight Adult Population (%)")
    axs[1][1].set_xlabel("Overweight Adult Population (%)")

    axs[0][0].set_ylabel("Aerobic exercise (%)")
    axs[1][0].set_ylabel("Muscle exercise (%)")
    axs[0][1].set_ylabel("Aerobic exercise (%)")
    axs[1][1].set_ylabel("Muscle exercise (%)")

    fig.tight_layout()

    fig.legend([
        'Obese adults, ≥150 min Aerobic Activity (%)',
        'Obese adults, Muscle Strengthening ≥ 2x/wk (%)',
        'Overweight adults, ≥150 min Aerobic Activity (%)',
        'Overweight adults, Muscle Strengthening ≥ 2x/wk (%)'
    ], loc='upper right', bbox_to_anchor=(1, 0.94))

    fig.suptitle("Weekly Exercise vs. Weight Class")
    fig.subplots_adjust(top=0.72)

    plot_correlation(
        df2[QCol.OBESITY_18_PLUS.value],
        df2['AVG_EXERCISE_AEROBIC'],
        axs[0][0],
        "tab:blue"
    )

    plot_correlation(
        df2[QCol.OBESITY_18_PLUS.value],
        df2['AVG_EXERCISE_MUSCLE'],
        axs[1][0],
        "tab:orange"
    )

    plot_correlation(
        df2[QCol.OVERWEIGHT_18_PLUS.value],
        df2['AVG_EXERCISE_AEROBIC'],
        axs[0][1],
        "tab:green"
    )

    plot_correlation(
        df2[QCol.OVERWEIGHT_18_PLUS.value],
        df2['AVG_EXERCISE_MUSCLE'],
        axs[1][1],
        "tab:red"
    )

    plt.savefig('./figures/fig8_weight_class_vs_aerobic_exercise.png', dpi=300)

    plt.show()

if __name__ == "__main__":
    visualisation6()
