import pandas as pd
import json
from sqlalchemy import types
import warnings

from lib.db import ENGINE, SQLITE_FILE_FILENAME

DATASET1_FILENAME="datasets/physical-activity.json"
DATASET2_FILENAME="datasets/walkability-index.csv"

def process_df1():
    print("Processing dataset 1...")

    # ------------
    # Loading Data
    # ------------

    print(f"Loading data from file '{DATASET1_FILENAME}'...")

    with open(DATASET1_FILENAME, mode='r') as file:
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
        'LocationID' # FIPS state code, not useful since we have LocationAbbr
    ]

    # Remove unneeded cols
    df.drop(to_drop, inplace=True, axis="columns")
    print("1. Removed unneeded cols from DataFrame")

    # YearStart and YearEnd should be identical, so merge them into one col called Year
    mask = df['YearStart'] != df['YearEnd']

    # If there is a row where YearStart and YearEnd are not equal, throw this error
    if (mask.sum() != 0):
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html
        bad_rows = df.loc[mask]
        warnings.warn(f"YearStart and YearEnd do not match for some rows: {bad_rows}")

    # Set a year column just to year start
    df['Year'] = df['YearStart']
    df.drop(['YearStart', 'YearEnd'], inplace=True, axis=1)
    print("2. Merged YearStart and YearEnd columns")


    # Flag indicating missing data
    df["MissingData"] = df["Data_Value_Footnote"].notna()
    df.drop(
        [ "Data_Value_Footnote", "Data_Value_Footnote_Symbol" ], 
        inplace=True, 
        axis="columns"
    )
    print("3. Flag for missing data column")


    # We can safely remove these since Stratification info gives these to us anyway.
    df.drop([
        "Age(years)",
        "Education",
        "Sex",
        "Income",
        "Race/Ethnicity",
    ], inplace=True, axis="columns")
    print("4. Remove duplicate stratification info")

    # Remove duplicate Data_Value_Alt col. Show warning if not identical.
    # https://stackoverflow.com/a/73011295
    results = df.query('Data_Value.notnull() & Data_Value != Data_Value_Alt')
    if (results.size > 0):
        warnings.warn(f"Data_Value and Data_Value_Alt not identical for some rows: {results}")

    df.drop(['Data_Value_Alt'], inplace=True, axis="columns")


    print("Finished cleaning DataFrame")

    return df

    # ----------------
    # Save to database
    # ----------------
    
    print('Saving to SQLite database...')

    

    print(f"Saved to '{SQLITE_FILE_FILENAME}'")


def process_df2():
    print("Processing dataset 2...")

    # -------------------
    # Process 2nd dataset
    # -------------------

    print(f"Loading data from file '{DATASET2_FILENAME}'...")

    with open(DATASET2_FILENAME, mode='r') as file:
        print(f"Creating Pandas DataFrame with data...")

        df2 = pd.read_csv(file)

    # -------------
    # Cleaning Data
    # -------------

    print("Cleaning data...")

    # Remove all cols except state and walk index
    # https://stackoverflow.com/a/53214704
    df2 = df2.filter(['STATEFP', 'NatWalkInd'])
    print("1. Removed unneeded cols from DataFrame")

    df2 = df2.groupby("STATEFP", as_index=False)["NatWalkInd"].mean().to_frame()
    print("2. Averaged state walkability by mean")

    # https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code
    fp_map = {
        1: "AL",
        2: "AK",
        4: "AZ",
        5: "AR",
        6: "CA",
        8: "CO",
        9: "CT",
        10: "DE",
        11: "DC",
        12: "FL",
        13: "GA",
        15: "HI",
        16: "ID",
        17: "IL",
        18: "IN",
        19: "IA",
        20: "KS",
        21: "KY",
        22: "LA",
        23: "ME",
        24: "MD",
        25: "MA",
        26: "MI",
        27: "MN",
        28: "MS",
        29: "MO",
        30: "MT",
        31: "NE",
        32: "NV",
        33: "NH",
        34: "NJ",
        35: "NM",
        36: "NY",
        37: "NC",
        38: "ND",
        39: "OH",
        40: "OK",
        41: "OR",
        42: "PA",
        44: "RI",
        45: "SC",
        46: "SD",
        47: "TN",
        48: "TX",
        49: "UT",
        50: "VT",
        51: "VA",
        53: "WA",
        54: "WV",
        55: "WI",
        56: "WY"
    }

    df2['LocationAbbr'] = df2['STATEFP'].map(fp_map)

    # Remove rows not in dict
    df2.dropna(inplace=True)

    print("3. Attached state alphanumeric as LocationAbbr")
    
    df2.rename(columns={ 'NatWalkInd': 'Walkability_Index' }, inplace=True)
    print ("4. Renamed NatWalkInd into Walkability_Index")

    df2.drop(axis='columns', labels=['STATEFP'], inplace=True)

    print("4. Removed old STATEFP col")

    print("Finished cleaning DataFrame 2")

    return df2

def merge_datasets(df1, df2):
    print("Mering DataFrames on LocationAbbr...")
    df = pd.merge(df1, df2, on='LocationAbbr', how='left')

    print("Saving merged DataFrame to DB...")
    df.to_sql(
        "merged_dataset",
        con=ENGINE,
        if_exists="replace",
        index=True,
        dtype={
            'LocationAbbr': types.TEXT,
            'LocationDesc': types.TEXT,
            'Class': types.TEXT,
            'Topic': types.TEXT,
            'Question': types.TEXT,
            'Data_Value_Unit': types.TEXT,
            'Data_Value': types.FLOAT,
            'Low_Confidence_Limit': types.FLOAT,
            'High_Confidence_Limit': types.FLOAT,
            'Sample_Size': types.REAL,
            'Total': types.TEXT,
            'ClassID': types.TEXT,
            'TopicID': types.TEXT,
            'QuestionID': types.TEXT,
            'DataValueTypeID': types.TEXT,
            'StratificationCategory1': types.TEXT,
            'Stratification1': types.TEXT,
            'StratificationCategoryId1': types.TEXT,
            'StratificationID1': types.TEXT,
            'Year': types.NUMERIC,
            'MissingData': types.BOOLEAN,
            'Walkability_Index': types.FLOAT,
        }
    )

    print("Finished saving DataFrame to DB!")

def process_datasets():
    df1 = process_df1()
    df2 = process_df2()
    
    merge_datasets(df1, df2)

if __name__ == "__main__":
    process_datasets()