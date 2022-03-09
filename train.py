import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from file_operations.file_operations import FileOperation
from data_validation.data_validator import data_validation
from data_preprocessing.data_preprocessor import data_preprocessing
from best_model_finder.best_model_finder import BestModelFinder

df = pd.read_csv("DATA/flight_fare_20211221_120000.csv")


def training(df):
    try:
        file_operation = FileOperation()
        df = data_validation(df)

        # If the data is validated save the data in the input.csv file
        success_message = file_operation.save_df(df, 'input')

        if type(success_message) == str:
            print("Data Validation Successful")

            df = file_operation.load_df('input')

            print(df.shape)

            df = data_preprocessing(df)
            print("preprocessing done!")

            if type(df) == pd.core.frame.DataFrame:

                print("Separating Features and labels")
                X = df.drop(columns="Price")
                y = df["Price"]

                print("Spliting training and testing sets")

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

                print("Model Training, finding the best model")
                best_model_finder = BestModelFinder(X, y, X_train, y_train, X_test, y_test)

                best_model, model_name, model_score = best_model_finder.get_best_model()

                # Saving model
                print("Saving the best model")

                file_operation.save_model(best_model, 'best_model')

                print("\n\n\nSuccessfully completed the training process")

                return f"Training Successful! Your model: {model_name}; model score: {model_score:0.2f}",  # comma to return it as tuple

            else:
                return "Data Processing Failed!"
        else:
            return "Invalid Dataset"
    except:
        return "Training Failed due to an error!"
