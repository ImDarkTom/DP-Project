import pandas
from sqlalchemy import create_engine

SQLITE_FILE_FILENAME="data.sqlite"

ENGINE = create_engine(f'sqlite:///{SQLITE_FILE_FILENAME}', echo=False)

def load_df_from_db(table_name: str):
    return pandas.read_sql_table(
        table_name,
        con=ENGINE,
        index_col="index",
    )