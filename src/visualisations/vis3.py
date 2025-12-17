import pandas as pd

from src.enums import QCol, Strat

def visualisation3(df: pd.DataFrame):
    # After exploration 2023 is the latest date that has exercise data
    df2 = df[
        (df['YEAR'] == 2023) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][[
        'YEAR', 
        QCol.WALKABILITY_INDEX.value,
        QCol.MOD_AEROBIC_150_MIN.value,
        QCol.MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS.value,
        QCol.MOD_AEROBIC_300_MIN.value,
        QCol.MUSCLE_2_DAYS.value
    ]]
    
    print(df2)

if __name__ == "__main__":
    from src.lib.db import load_df_from_db

    visualisation3(load_df_from_db())
