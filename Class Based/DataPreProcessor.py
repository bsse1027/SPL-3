import numpy as np
import pandas as pd
from pandas import json_normalize
import json


class DataPreProcess:

    def load_df(self, csv_path, nrows=None):
        json_cols = ['device', 'geoNetwork', 'totals', 'trafficSource']
        df = pd.read_csv(csv_path,
                         # converters are dict of functions for converting values in certain columns. Keys can either be integers or column labels.
                         # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
                         # It is mainly used for deserializing native string, byte, or byte array which consists of JSON data into Python Dictionary.
                         converters={col: json.loads for col in json_cols},
                         dtype={'fullVisitorId': 'str'},  # Important!!
                         nrows=nrows)
        for col in json_cols:
            # for each column, flatten data frame such that the values of a single col are spread in different cols
            # This will use subcol as names of flat_col.columns
            flat_col = json_normalize(df[col])
            # Name the columns in this flatten data frame as col.subcol for tracability
            flat_col.columns = [f"{col}.{subcol}" for subcol in flat_col.columns]
            # Drop the json_col and instead add the new flat_col
            df = df.drop(col, axis=1).merge(flat_col, right_index=True, left_index=True)
        df.to_csv('pre_processed.csv')
        return df

