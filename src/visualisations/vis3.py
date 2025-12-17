import pandas as pd

from src.enums import QCol, Strat

def visualisation3(df: pd.DataFrame):
    df2 = df[
        (df['YEAR'] == 2024) &
        (df['STRATIFICATION'] == Strat.OVERALL.value)
    ][['YEAR', QCol.OBESITY_18_PLUS.value, QCol.OVERWEIGHT_18_PLUS.value]]
    
    print(df2)

if __name__ == "__main__":
    from src.lib.db import load_df_from_db

    visualisation3(load_df_from_db())
