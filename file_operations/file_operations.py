# Including dataframe operations and zipfiles to download

from joblib import dump, load
import os
import shutil
import pandas as pd
import zipfile


class FileOperation:
    """
    This class is used to save a model, load a model, and find the correct model to load.
    """

    def __init__(self):
        if 'app.py' in os.listdir(os.getcwd()):
            self.model_directory = "models/"
            self.df_directory = "DATA/"
        else:
            self.model_directory = "../models/"
            self.df_directory = "../DATA/"

    def save_model(self, model, filename):
        path = os.path.join(self.model_directory, filename)
        if os.path.isdir(path):
            # If there is an existing model in the same location, delete it.
            shutil.rmtree(path)
            # And create a new folder for the model
            os.makedirs(path)
        else:
            os.makedirs(path)

        # Creating a the model in a folder same as the filename
        dump(value=model, filename=path + '/' + filename + '.joblib')

    def load_model(self, filename):
        path = os.path.join(self.model_directory, filename)
        model = load(filename=path+'/'+filename+'.joblib')
        return model


    def save_df(self, df, filename):
        try:
            path = self.df_directory
            if not os.path.isdir(path):
                os.makedirs(path)

            # Check if there is any file with {filename}

            files = os.listdir(path)
            filepath = os.path.join(path, f"{filename}.csv")

            if f"{filename}.csv" in files:
                # If yes: load it as data
                data = pd.read_csv(filepath)
            else:
                # else: find csv file with filename flight_fare and load it as data
                data = pd.read_csv(os.path.join('DATA', "flight_fare.csv"))

            # Concat both data and df, if there is any error while concatinating, return "Data Validation Failed"
            df = pd.concat([data, df], axis=0)

            # Due to change in the datatypes of datetime, it's creating more records
            df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'])

            # Remove the duplicate rows
            df = df.drop_duplicates(keep='first')
            # save the file with filename
            df.to_csv(filepath, index = False)
            print(df.shape)
            return "File added Successfully"
        except:
            print("Error occurred")
            pass

    def load_df(self, filename):
        try:
            if not os.path.isdir(self.df_directory):
                os.makedirs(self.df_directory)
            filepath = os.path.join(self.df_directory, f"{filename}.csv")
            if os.path.exists(filepath):
                print(f"File with filepath: {filepath} exists.")
                df = pd.read_csv(filepath)
                return df
            else:
                print(f"No file with filepath: {filepath} exists. Loading the backup flight_fare.csv file")
                df = pd.read_csv(os.path.join('DATA', 'flight_fare.csv'))
                return df
        except:
            pass

# res = training(df)

def to_download(res):
    if type(res) == tuple:
        # Zip the file and save it for downloading

        shutil.make_archive('comp_file','zip','models')
        comp_file = zipfile.ZipFile('comp_file.zip','a')
        comp_file.write("logs.txt",compress_type=zipfile.ZIP_DEFLATED)
        comp_file.close()

    elif type(res) == str:
        if res == "Data Processing Failed!":
            # Dowload logs
            comp_file = zipfile.ZipFile('comp_file.zip','w')
            comp_file.write("logs.txt",compress_type=zipfile.ZIP_DEFLATED)
            comp_file.close()

        elif res == "Invalid Dataset":
            # Download Schema files
            comp_file = zipfile.ZipFile('comp_file.zip','w')
            comp_file.write("required_datatypes.txt",compress_type=zipfile.ZIP_DEFLATED)
            comp_file.close()
        else:
            # Download logs and schema files
            comp_file = zipfile.ZipFile('comp_file.zip','w')
            comp_file.write("logs.txt",compress_type=zipfile.ZIP_DEFLATED)
            comp_file.write("required_datatypes.txt",compress_type=zipfile.ZIP_DEFLATED)
            comp_file.close()
