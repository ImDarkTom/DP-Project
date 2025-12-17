import pandas
from sqlalchemy import create_engine

SQLITE_FILE_FILENAME="db.sqlite"

ENGINE = create_engine(f'sqlite:///{SQLITE_FILE_FILENAME}', echo=False)

def load_df_from_db():
    return pandas.read_sql_table(
        "merged_dataset",
        con=ENGINE,
        index_col="index",
    )