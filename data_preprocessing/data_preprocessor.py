import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import mutual_info_regression, SelectPercentile
from file_operations.file_operations import FileOperation


class DataPreprocessor:

    def __init__(self):
        pass

    # Drop null values

    def drop_null(self, df):
        try:
            df = df.dropna(axis=0)
            return df
        except:
            pass

    # Drop: 'Additional_Info', 'Route'

    def drop_cols(self, df, *cols):
        if cols is not None:
            #             cols = list(cols)
            # what if these columns are not present in the dataset.
            drop_cols = []
            for col in cols:
                if col in df.columns:
                    drop_cols.append(col)
            return df.drop(columns=drop_cols)
        else:
            return df

    # Extract time from "Arrival_Time" and "Departure_Time" cols

    def extract_time(self, t):  # Dependent
        t = t.split()
        for i in t:
            if ':' in i:
                return i
        return np.nan

    def get_arr_time(self, df):  # Independent
        try:
            if is_numeric_dtype(df['Arrival_Time']):
                return df
            else:
                arr_time = df["Arrival_Time"].apply(self.extract_time)
                if arr_time.isnull().sum() == 0:
                    df["Arrival_Time"] = arr_time
                    return df
                elif arr_time.isnull().sum() / len(df["Arrival_Time"]) >= 0.3:
                    return "Invalid data in Arrival_Time column"
                else:
                    df['Arrival_Time'] = arr_time
                    print(f"{arr_time.isnull().sum()} rows are missing after extracting time from Arrival_Time column")
                    df = df.dropna(axis=0)
                    return df
        except:
            pass

    def get_dep_time(self, df):  # Independent
        try:
            if is_numeric_dtype(df['Dep_Time']):
                return df
            else:
                dep_time = df["Dep_Time"].apply(self.extract_time)
                if dep_time.isnull().sum() == 0:
                    df["Dep_Time"] = dep_time
                    return df
                elif dep_time.isnull().sum() / len(df["Dep_Time"]) >= 0.3:
                    return "Invalid data in Dep_Time column"
                else:
                    df['Dep_Time'] = dep_time
                    print(f"{dep_time.isnull().sum()} rows are missing after extracting time from Dep_Time column")
                    df = df.dropna(axis=0)
                    return df
        except:
            pass

    # Round time: "Dep_Time", "Arrival_Time"

    def round_time(self, t):  # Dependent
        t = t.split(":")
        res = int(t[0]) + int(t[1]) / 60
        return round(res)

    def round_arr_time(self, df):  # Independent
        try:
            if is_numeric_dtype(df['Arrival_Time']):
                return df
            else:
                df = self.get_arr_time(df)
                if type(df) == pd.core.frame.DataFrame:
                    df["Arrival_Time"] = df["Arrival_Time"].apply(self.round_time)
                    return df
                else:
                    return "Error in getting arrival time from 'Arrival_Time' column in round_arr_time method"
        except:
            pass

    def round_dep_time(self, df):  # Independent
        try:
            if is_numeric_dtype(df['Dep_Time']):
                return df
            else:
                df = self.get_dep_time(df)
                if type(df) == pd.core.frame.DataFrame:
                    df["Dep_Time"] = df["Dep_Time"].apply(self.round_time)
                    return df
                else:
                    return "Error in getting departure time from 'Dep_Time' column in round_dep_time method"
        except:
            pass

    # Convert to numbers: "Total_Stops"

    def get_stops(self, df):  # Independent
        try:
            df = df.dropna(axis=0)
            if is_numeric_dtype(df["Total_Stops"]):
                return df
            else:
                stops = df["Total_Stops"].replace(to_replace='non-stop', value='0').apply(lambda x: int(x[0]))
                if stops.isnull().sum() == 0:
                    df["Total_Stops"] = stops
                    return df
                elif stops.isnull().sum() / len(df["Total_Stops"]) >= 0.3:
                    return "Invalid data in Total_Stops column"
                else:
                    df['Total_Stops'] = stops
                    print(f"{stops.isnull().sum()} rows are missing after extracting time from Total_Stops column")
                    df = df.dropna(axis=0)
                    return df
        except:
            pass

    # Convert to minutes: "Duration"

    def total_minutes(self, t):  # Dependent
        t = t.lower()
        t = t.split()
        if len(t) == 1:
            if 'h' in t[0]:
                t = int(t[0].replace('h', '')) * 60
            else:
                t = int(t[0].replace('m', ''))
        else:
            t = int(t[0].replace('h', '')) * 60 + int(t[1].replace('m', ''))
        return t

    def minutes_duration(self, df):  # Independent
        try:
            if is_numeric_dtype(df["Duration"]):
                return df
            else:
                df['Duration'] = df['Duration'].apply(self.total_minutes)
                return df
        except:
            pass

    # Extract datetime information: "Date_of_Journey"

    #     def quarter(self, df):                           # Dependent
    #         date, days_in_month = df['date'], df['days_in_month']
    #         q = days_in_month/4
    #         diff = days_in_month - date
    #         return int(4 - (diff//q))

    def extract_datetime_data(self, df):  # Independent
        try:
            df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'])
            df['day'] = df['Date_of_Journey'].dt.day_name()  # One hot encoding is required
            df['date'] = df['Date_of_Journey'].dt.day  #
            df['month'] = df['Date_of_Journey'].dt.month  #
            df['weekend'] = df['day'].apply(
                lambda x: 1 if x in ["Sunday", "Saturday"] else 0)  # Will be removed in feature selection step
            df['days_in_month'] = df['Date_of_Journey'].dt.days_in_month
            #             df['quarter'] = df.apply(self.quarter, axis=1)  # Getting 0.98 collinearity with date
            df = df.drop(columns=['days_in_month', 'Date_of_Journey'])
            return df
        except:
            pass

    # Categorical encode: 'Airline', "Source", "Destination"

    def categorical_encoding(self, df):
        try:
            ohc = OneHotEncoder(sparse=False)

            #             cols = ['Airline', "Source", "Destination"]

            cols = []

            for col in ['Airline', "Source", "Destination", 'day']:
                try:
                    # If these cols are already encoded, there will an error when you perform this opertion
                    if not is_numeric_dtype(df[col]):
                        cols.append(col)
                except:
                    continue
            print(cols)

            if len(cols) > 0:
                enc_data = ohc.fit_transform(df[cols])  #
                enc_cols = ohc.get_feature_names_out()
                enc_df = pd.DataFrame(data=enc_data, columns=enc_cols, index=df.index)  #

                df = df.drop(columns=cols)

                df = pd.concat([df, enc_df], axis=1)

                # Save the model
                file_operations = FileOperation()
                file_operations.save_model(ohc, "OHE")
                return df

            return df

        except:
            pass

    # Feature Selection

    def correlation(self, df, threshold):  # Dependent # Dependent
        # Multicollinearity check
        col_corr = set()  # Set of all the names of correlated columns
        corr_matrix = df.corr()
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    colname = corr_matrix.columns[i]  # getting the name of column
                    col_corr.add(colname)
        return col_corr

    def remove_multicollinearity(self, X):  # Dependent
        # Remove multicollinearity
        try:
            drop_cols = self.correlation(X, 0.9)  # Taking threshold as 0.9
            if len(drop_cols) > 0:
                X = X.drop(columns=drop_cols)
                return X
            return X
        except:
            pass

    def mutual_info_selection(self, df, percentile):  # Dependent
        # Mutual information check
        try:
            X = df.drop(columns="Price")
            y = df["Price"]
            selected_top_columns = SelectPercentile(mutual_info_regression, percentile=percentile)
            selected_top_columns.fit(X, y)
            selected_cols = X.columns[selected_top_columns.get_support()]
            X = X[selected_cols]
            X['Price'] = y
            df = X
            return df
        except:
            pass

    def feature_selection(self, df):  # Independent
        # Compilation
        try:
            X = df.drop(columns="Price")
            y = df["Price"]

            # Remove multicollinearity
            X = self.remove_multicollinearity(X)
            X['Price'] = y
            df = X

            # Remove features with less information
            df = self.mutual_info_selection(df,
                                            50)  # Consider features in top 50 percentile in terms of mutual information

            # Return Dataframe
            return df

        except:
            pass


def data_preprocessing(df):
    data_preprocessor = DataPreprocessor()

    while type(df) == pd.core.frame.DataFrame:
        df = data_preprocessor.drop_null(df)
        df = data_preprocessor.drop_cols(df, 'Additional_Info', 'Route')
        df = data_preprocessor.get_arr_time(df)
        df = data_preprocessor.get_dep_time(df)
        df = data_preprocessor.round_arr_time(df)
        df = data_preprocessor.round_dep_time(df)
        df = data_preprocessor.get_stops(df)
        df = data_preprocessor.minutes_duration(df)
        df = data_preprocessor.extract_datetime_data(df)
        df = data_preprocessor.categorical_encoding(df)
        df = data_preprocessor.feature_selection(df)
        return df
    return df
