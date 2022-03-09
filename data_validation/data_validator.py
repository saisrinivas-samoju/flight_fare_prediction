# Initial validation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class DataValidator:

    def __init__(self):
        pass

    def drop_null(self, df):
        try:
            df = df.dropna(axis=0)
            for i in df.shape:
                if i > 0:
                    continue
                else:
                    return "Failed in initial data validation, Either one or more columns has all null values or no values in the dataset"
            return df
        except:
            pass

    def validate_col_len(self, df):
        # Column length validation
        try:
            if df.shape[1] == 11:
                return df
            else:
                return "Failed in initial data validation, Check the number of columns in your dataset"
        except:
            pass

    def validate_col_names(self, df):
        # Column name validation
        try:
            valid = set(df.columns) == set(
                ['Airline', 'Date_of_Journey', 'Source', 'Destination', 'Route', 'Dep_Time', 'Arrival_Time', 'Duration',
                 'Total_Stops', 'Additional_Info', 'Price'])
            if valid:
                return df
            else:
                return "Failed in initial data validation, Check the names of the columns in your dataset"
        except:
            pass

    def validate_col_dtype_initial(self, df):
        try:
            # Column datatype validation
            dtype_validation = all([df.dtypes['Airline'] == np.dtype("O"),
                                    df.dtypes['Date_of_Journey'] == np.dtype("O") or df.dtypes[
                                        'Date_of_Journey'] == np.dtype('<M8[ns]'),
                                    df.dtypes['Source'] == np.dtype("O"),
                                    df.dtypes['Destination'] == np.dtype("O"),
                                    df.dtypes['Route'] == np.dtype("O"),
                                    df.dtypes['Dep_Time'] == np.dtype("O"),
                                    df.dtypes['Arrival_Time'] == np.dtype("O"),
                                    df.dtypes['Duration'] == np.dtype("O"),
                                    df.dtypes['Total_Stops'] == np.dtype("O"),
                                    df.dtypes['Additional_Info'] == np.dtype("O"),
                                    df.dtypes['Price'] == np.dtype('int64')])
            if dtype_validation == False:
                return "Failed in initial data validation, Please check your column datatypes and upload it again."
            else:
                # dropping missing values
                res = self.drop_null(df)
                if type(res) != str:
                    df = res
                    try:
                        df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'])
                        return df
                    except:
                        return "Failed in initial data validation, Please check the data in 'Date_of_Journey' column."
                else:
                    return res
        except:
            pass

    def valid_duration(self, d):
        spaces = 0
        digits = 0
        alphas = 0
        for i in d:
            if i.isspace():
                spaces += 1
            elif i.isalpha():
                alphas += 1
            elif i.isdigit():
                digits += 1
            else:
                pass
        if len(d) != spaces + digits + alphas:
            return True

        d = d.split()
        for i in d:
            if not i[:-1].isdigit():
                return True
            else:
                if i[-1].lower() == 'h' or i[-1].lower() == 'm':
                    return False
                else:
                    return True

    def validate_duration(self, df):
        try:
            invalid_rows = df['Duration'].apply(self.valid_duration).sum()
            if invalid_rows == 0:
                return df
            else:
                return "Failed in initial data validation, Please check the data in 'Date_of_Journey' column."
        except:
            pass

    def valid_stops(self, s):
        s = s.lower()
        if s == 'non-stop':
            return False
        else:
            if s == "1 stop":
                return False
            else:
                if s.split()[0].isdigit() and s.split()[1] == 'stops':
                    return False
                else:
                    return True

    def validate_stops(self, df):
        try:
            invalid_rows = df["Total_Stops"].apply(self.valid_stops).sum()
            if invalid_rows == 0:
                return df
            else:
                return "Failed in initial data validation, Please check the data in 'Total_Stops' column."
        except:
            pass

    def valid_time(self, t):
        if t.count(':') == 1:
            items = t.split()
            for i in items:
                if ':' in i:
                    t = i
            if len(t) == 5:
                for j in range(5):
                    if j == 2:
                        if t[j] != ":":
                            return True
                    else:
                        if not t[j].isdigit():
                            return True
                return False
            else:
                return True
        else:
            return True

    def validate_dep_time(self, df):
        try:
            invalid_rows = df["Dep_Time"].apply(self.valid_time).sum()
            if invalid_rows == 0:
                return df
            else:
                return "Failed in initial data validation, Please check the data in 'Dep_Time' column."
        except:
            pass

    def validate_arr_time(self, df):
        try:
            invalid_rows = df["Arrival_Time"].apply(self.valid_time).sum()
            if invalid_rows == 0:
                return df
            else:
                return "Failed in initial data validation, Please check the data in 'Arrival_Time' column."
        except:
            pass

def data_validation(df):
    validator = DataValidator()
    while type(df)!=str:
        df = validator.validate_col_len(df)
        df = validator.validate_col_names(df)
        df = validator.validate_col_dtype_initial(df)
        df = validator.validate_duration(df)
        df = validator.validate_stops(df)
        df = validator.validate_dep_time(df)
        df = validator.validate_arr_time(df)
        print("Initial Data Validation Successful")
        return df
    return df