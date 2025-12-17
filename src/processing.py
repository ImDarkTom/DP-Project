import pandas as pd
import json
from sqlalchemy import types
import warnings

from src.lib.db import ENGINE, SQLITE_FILE_FILENAME

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
        'LocationDesc', # We have this in enum format via LocationAbbr
        'Class', # not useful
        'ClassID',
        'Topic', # not useful
        'TopicID',
        'StratificationCategory1', # not useful
        'Stratification1', # Rendundant since we have StratificationID1 and the enum giving us info
        'DataValueTypeID', # Always 'VALUE'
        'Question', # Redundant since we have QuestionID and the enum giving us info
        'Datasource', # always 'Behavioral Risk Factor Surveillance System'
        'Data_Value_Type', # always 'Value',
        'Data_Value_Unit', # added on data after 2023. Seems to be useless since all 'Data_Value's are percentages
        'GeoLocation', # not useful for our purposes
        'LocationID', # FIPS state code, not useful since we have LocationAbbr
        'Total', # Seems to just be 'TOTAL' if the stratification is 'OVERALL'
        'Sample_Size', # we don't use this
        'StratificationCategoryId1', # strat category ID, we don't use this 
        'Low_Confidence_Limit', # we don't use this
        'High_Confidence_Limit ' # we don't use this
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
    df.drop(['YearStart', 'YearEnd'], inplace=True, axis="columns")
    print("2. Merged YearStart and YearEnd columns")

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

    # Pivot to better format data, based on `tests/test.py`
    df = df.pivot(index=['LocationAbbr', 'StratificationID1', 'Year'], columns='QuestionID', values='Data_Value')

    # rename indexes
    # https://stackoverflow.com/a/41221249
    df.index.set_names(['LOCATION', 'STRATIFICATION', 'YEAR'], inplace=True)

    df.rename(columns={
        'Q018': 'FRUIT_LT_ONCE_DAILY',
        'Q019': 'VEG_LT_ONCE_DAILY',
        'Q036': 'OBESITY_18_PLUS',
        'Q037': 'OVERWEIGHT_18_PLUS',
        'Q043': 'MOD_AEROBIC_150_MIN',
        'Q044': 'MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS',
        'Q045': 'MOD_AEROBIC_300_MIN',
        'Q046': 'MUSCLE_2_DAYS',
        'Q047': 'NO_LEISURE_PHYS_ACTIVITY',
    }, inplace=True)

    # https://www.geeksforgeeks.org/pandas/reverting-from-multiindex-to-single-index-dataframe-in-pandas/
    df.reset_index(['LOCATION', 'STRATIFICATION', 'YEAR'], inplace=True)

    print("Finished cleaning DataFrame")

    return df

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

    df2 = df2.groupby("STATEFP", as_index=False)["NatWalkInd"].mean()
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

    df2['LOCATION'] = df2['STATEFP'].map(fp_map)

    # Remove rows not in dict
    df2.dropna(inplace=True)
    print("3. Attached state alphanumeric as LocationAbbr")
    

    df2.rename(columns={ 'NatWalkInd': 'WALKABILITY_INDEX' }, inplace=True) # type: ignore
    print ("4. Renamed NatWalkInd into WALKABILITY_INDEX")


    df2.drop(axis='columns', labels=['STATEFP'], inplace=True)
    print("4. Removed old STATEFP col")

    df2.set_index('LOCATION', inplace=True)

    print("Finished cleaning DataFrame 2")

    return df2

def merge_datasets(df1: pd.DataFrame, df2: pd.Series):
    print("Mering DataFrames on LOCATION...")
    
    df = df1.merge(df2, on='LOCATION', how='left')

    print('Saving merged DataFrame to SQLite database...')
    
    df.to_sql(
        "merged_dataset",
        con=ENGINE,
        if_exists="replace",
        index=True,
        dtype={
            'LOCATION': types.TEXT,
            'STRATIFICATION': types.TEXT,
            'YEAR': types.NUMERIC,
            'OBESITY_18_PLUS': types.FLOAT,
            'OVERWEIGHT_18_PLUS': types.FLOAT,
            'MOD_AEROBIC_150_MIN': types.FLOAT,
            'MOD_AEROBIC_150_MIN_PLUS_MUSCLE_2_DAYS': types.FLOAT,
            'MOD_AEROBIC_300_MIN': types.FLOAT,
            'MUSCLE_2_DAYS': types.FLOAT,
            'NO_LEISURE_PHYS_ACTIVITY': types.FLOAT,
            'FRUIT_LT_ONCE_DAILY': types.FLOAT,
            'VEG_LT_ONCE_DAILY': types.FLOAT,
            'WALKABILITY_INDEX': types.FLOAT,
        }
    )

    print(f"Saved to '{SQLITE_FILE_FILENAME}'")


def process_datasets():
    df1 = process_df1()
    print("===== DF2 =====")
    df2 = process_df2()

    print('===== MERGE =====')
    merge_datasets(df1, df2)

if __name__ == "__main__":
    process_datasets()