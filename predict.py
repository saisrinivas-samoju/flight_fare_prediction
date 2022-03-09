# Creating function from the above steps
import pandas as pd
from file_operations.file_operations import FileOperation

def get_prediction(user_input):
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6:'Sunday'}
    data = dict()
    ### For OHE ####
    data['Airline'] = [user_input["Airline"]]
    data["Source"] = [user_input["Source"]]
    data["Destination"] = [user_input["Destination"]]
    data["day"] = [day_dict[user_input["Date_of_Journey"].weekday()]]
    ################
    data["Dep_Time"] = [round(user_input['Dep_Time'].hour + user_input['Dep_Time'].minute/60)]
    data['Arrival_Time'] = [round(((((user_input['Dep_Time'].hour) * 60) + user_input['Dep_Time'].minute) + (((user_input['Duration'].hour) * 60) + user_input['Duration'].minute))/60)]
    data['Duration'] = [(user_input['Duration'].hour)*60 + user_input['Duration'].minute]
    data["Total_Stops"] = [user_input["Total_Stops"]]
    data["date"] = [user_input["Date_of_Journey"].day]
    data["month"] = [user_input["Date_of_Journey"].month]

    input_df = pd.DataFrame(data)

    file_operations = FileOperation()
    model = file_operations.load_model("best_model")
    ohe = file_operations.load_model("OHE")

    # Columns to encode
    to_enc_cols = ohe.feature_names_in_
    enc_data = ohe.transform(input_df[to_enc_cols])
    enc_cols = ohe.get_feature_names_out()
    enc_df = pd.DataFrame(data = enc_data, columns=enc_cols)
    enc_df

    # Dropping encoded columns
    input_df = input_df.drop(columns = to_enc_cols)

    input_df = pd.concat([input_df, enc_df], axis = 1)

    # Selected Features
    input_df = input_df[model.feature_names_in_]

    # Prediction
    prediction = int(round(model.predict(input_df)[0]/100)*100)

    return prediction
