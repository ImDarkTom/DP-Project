import pandas as pd
import json
from sqlalchemy import create_engine

SQLITE_FILE_FILENAME="data.sqlite"
DATASET_FILENAME="datasets/physical-activity.json"

# ------------
# Loading Data
# ------------

print(f"Loading data from file '{DATASET_FILENAME}'...")

with open(DATASET_FILENAME, mode='r') as file:
    data = json.load(file)

column_names: list[str] = list(map(lambda x: x['name'], data['meta']['view']['columns']))

print(f"Creating Pandas DataFrame with data...")

df = pd.DataFrame(data['data'], columns=column_names)

# -------------
# Cleaning Data
# -------------

print("Cleaning data...")

to_drop: list[str] = [ 
    'sid', # just identifies each row
    'id', # identifies each row
    'position', # always 0, pointless data
    'created_at', # always 1765553420
    'created_meta', # always blank
    'updated_at', # always 1765553420
    'updated_meta', # always blank
    'meta', # always '{ }'
    'Datasource', # always 'Behavioral Risk Factor Surveillance System'
    'Data_Value_Type', # always 'Value',
    'GeoLocation', # not useful for our purposes
]

# Remove unneeded cols
df.drop(to_drop, inplace=True, axis=1)
print("1. Removed unneeded cols from DataFrame")


# YearStart and YearEnd should be identical, so merge them into one col called Year
mask = df['YearStart'] != df['YearEnd']

if (mask.sum() != 0):
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
    bad_rows = df.loc[mask]
    raise ValueError(
        f"YearStart and YearEnd do not match for some rows: {bad_rows}"
    )

# Set a year column just to year start
df['Year'] = df['YearStart']
df.drop(['YearStart', 'YearEnd'], inplace=True, axis=1)
print("2. Merged YearStart and YearEnd columns")


print("Finished cleaning DataFrame")

# Save to database
print('Saving to SQLite database...')

engine = create_engine(f'sqlite:///{SQLITE_FILE_FILENAME}', echo=False)

df.to_sql(
    "physical_activity",
    con=engine,
    if_exists="replace",
    index=True
)

print(f"Saved to '{SQLITE_FILE_FILENAME}'")