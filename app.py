import streamlit as st
import datetime
import json
from streamlit_lottie import st_lottie
from num2words import num2words
import pandas as pd
import os
from PIL import Image

from flight_info.get_status import get_flight_status            # get_flight_status(flight_code, datetime_obj)
from flight_info.get_details import get_flight_details          # get_flight_details(from_code, to_code, airline_code=None, datetime_obj)
from flight_info.get_details import get_flight_details_input    # get_flight_details_input(user_inp)
from predict import get_prediction
from train import training                                      # training(df)
from file_operations.file_operations import to_download
###################################### HEAD #############################################

st.set_page_config(page_title="Flight Fare Prediction", page_icon=':airplane:', layout='wide')

def load_animation(filepath: setattr):
    with open(filepath, 'r') as f:
        return json.load(f)

flight_animation = load_animation('static/json/flight_animation.json')
flight_details_animation = load_animation('static/json/flight_details_animation.json')
contact_animation = load_animation('static/json/contact_animation.json')

#########################################################################################
###################################### STYLE ############################################
def style(filename):
    with open(filename, 'r') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

style("static/css/style.css")
#########################################################################################
###################################### BODY #############################################

                  ################### Reference ######################
month_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

                  ################### Side bar ######################
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-family:Tahoma;'>Flight Status</h1>", unsafe_allow_html=True)
    with st.form("status_form"):
        flight_code = st.text_input(label= "Enter Flight Number", placeholder= "Example: 6E287")
        datetime_obj = st.date_input(label="Choose Departure Date", value=datetime.date.today())
        status_submit = st.form_submit_button("Get Status")
    if status_submit:
        if len(flight_code)==0:
            st.error("Please enter the Flight Number")
        else:
            print(flight_code)
            if len(str(datetime_obj))==0:
                st.error("Please enter the date of departure before submitting")
            else:
                print(datetime_obj)
                with st.spinner(text=f"Getting the status of {flight_code.upper()}"):
                    res = get_flight_status(flight_code, datetime_obj)
                found = res[0]
                flight= res[1]
                if found:
                    result = f"""
                    <div style='text-align: center'>
                      <h2>Flight Status : <strong>{flight['status']}</strong></h2>
                      <h3>Flight Number : <strong>{flight['flight_no']}</strong></h3>
                      <h3>Flight Name   : <strong>{flight['flight_name']}</strong></h3>
                      <h2>{flight['from_code']} ---> {flight['to_code']}</h2>
                    </div>
                    """
                    st.warning(f"Flight Status: {flight['status']}")
                    st.text(f"Flight Number : {flight['flight_no']}")
                    st.text(f"Flight Name   : {flight['flight_name']}")

                    st.success("Source:")
                    st.text(f"{flight['source_airport']}\n{flight['source_city']}")
                    st.text(f"Scheduled : {flight['sch_dep_time']}")
                    st.text(f"Estimated : {flight['est_dep_time']}")
                    st.text(f"Terminal  : {flight['dep_terminal']}")
                    st.text(f"Gate      : {flight['dep_gate']}")

                    st.info("Destination:")
                    st.text(f"{flight['destination_airport']}\n{flight['destination_city']}")
                    st.text(f"Scheduled : {flight['sch_arr_time']}")
                    st.text(f"Estimated : {flight['est_arr_time']}")
                    st.text(f"Terminal  : {flight['arr_terminal']}")
                    st.text(f"Gate      : {flight['arr_gate']}")

                else:
                    st.error("No result found!")

                  ################### Main page ######################

st.markdown("<h1 style='text-align: center; -webkit-text-stroke: 1px #7700ff; color: white; font-family:Verdana'>Flight Fare Prediction</h1>", unsafe_allow_html=True)
with st.container():
    left_column, right_column = st.columns((2, 1))
    with left_column:
        st.markdown("<h3 style='text-align: center; font-family:Tahoma;'>Predict Result & Check Available Flights &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; </h3>", unsafe_allow_html=True)
    with right_column:
        st.markdown("<h3 style='text-align: center; font-family:Tahoma'>Train model  &nbsp; &nbsp; &nbsp; &nbsp; </h3>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3, col4 = st.columns([1, 0.9, 0.1, 1.2])
    with st.container():
        with st.form("user_input"):
            with col1:
                airline = st.selectbox(label="\nSelect Airline Service", options = ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet','Multiple carriers', 'GoAir', 'Vistara', 'Air Asia','Vistara Premium economy', 'Jet Airways Business','Multiple carriers Premium economy', 'Trujet'])
                st.write("###")
                source = st.selectbox(label="Select Source", options = ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai'])
                st.write("###")
                date = st.date_input(label="Choose Departure Date", value=datetime.date.today())
                st.write("###")
                duration = st.slider(label="Set Comfortable Duration", min_value=datetime.time(1, 0), max_value= datetime.time(12, 0), value= datetime.time(2, 0))
                st.write("###")
            with col2:
                stops = st.number_input(label="Set Total Stops", min_value=0, max_value=4, value=0)
                st.write("###")
                destination = st.selectbox(label="Select Destination", options = ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad'])
                st.write("###")
                dep_time = st.time_input('Set Departure Time', datetime.datetime.now().time())
                st.write("###")
                flights = st.selectbox('Check the available flights from', ('All Available Airline Services', 'Selected Airline Service'))
                st.write("###")
            submit = st.form_submit_button("Calculate Flight Fare")

            ################ Submit Results END ##########################

    with col3:
        st.write("#")

####################### Training Block ##############################

    with col4:
        uploaded_file = None
        st.write("Download sample CSV file for reference and testing")
        if uploaded_file is None:
            with open(os.path.join('DATA','flight_fare.csv'), 'rb') as f:
                st.download_button('Download Sample File', f, file_name='sample_data.csv')
        uploaded_file = st.file_uploader(label="Upload your csv file for training", type = ['csv'])
        if uploaded_file is not None:
            print(uploaded_file)
            st.write("Click 'Train' button to start the training process")
            train_btn = st.button(label="Train")
            if train_btn:
                try:
                    with open('status.txt', 'r') as f:
                        status = f.read()
                except:
                    with open('status.txt', 'w') as f:
                        f.write('')
                if status=='static' or status=='':
                    try:
                        with open('status.txt', 'w') as f:
                            status = f.write("running")
                        df = pd.read_csv(uploaded_file)
                        with st.spinner(text="Machine Learning Model Training is in Progress..."):
                            res = training(df)
                        with st.spinner(text="Preparing your model related files for downloading"):
                            try:
                                to_download(res)   # creating the files for downloading
                                if type(res) == tuple:
                                    print(f"{res[0]}")
                                    st.success(res[0])
                                    with open('comp_file.zip', 'rb') as f:
                                        st.download_button('Download Files', f, file_name='your_files.zip')
                                else:
                                    st.error(res)
                            except:
                                st.error("Error occurred in preparing the files for downloading")
                        with open('status.txt', 'w') as f:
                            status = f.write("static")
                    except:
                        st.error("Error Occurred!")
                else:
                    st.warning("A Model Training Process is already in Progress. Please wait until it is done!")
        else:
            st_lottie(flight_animation, speed=1.5, reverse= False, loop= True, quality='high')
        st.write("#")

######################### END: Training Block ###########################

############################# START: Adding Submitted results in a separate container ################################
with st.container():
    left_col, center_line, right_col= st.columns([1.9, 0.1, 1.2])
    if submit:
        with left_col:
            # Add try and except blocks
            user_inp = {'Airline':airline, 'Date_of_Journey': date, 'Source': source, 'Destination':destination, 'Dep_Time':dep_time, 'Duration': duration, 'Total_Stops':stops, "flights":flights}
            print(user_inp)
            # Add try and except blocks
            with st.spinner(text="Predicting your Flight fare..."):
                prediction = get_prediction(user_inp)
                st.markdown(f'<h4 style="font-family:Tahoma;">Your flight fare is predicted to be: <span style="color:#7700ff; -webkit-text-stroke: 1px white;">{prediction} INR</span></h4>', unsafe_allow_html=True)
            # Add try and except blocks
            with st.spinner(text="Getting available flight details..."):
                inp = inp = get_flight_details_input(user_inp)
                detail_df = get_flight_details(inp[0], inp[1], inp[2], inp[3])
                if detail_df.shape[0]==0:
                    st.subheader(f"No flights available on {month_dict[user_inp['Date_of_Journey'].month]} {user_inp['Date_of_Journey'].day}, {user_inp['Date_of_Journey'].year}")
                else:
                    detail_df.index = detail_df.index + 1
                    if detail_df.shape[0]==1:
                        st.subheader(f"Only One flight is Available  on {month_dict[user_inp['Date_of_Journey'].month]} {user_inp['Date_of_Journey'].day}, {user_inp['Date_of_Journey'].year}")
                        st.dataframe(data=detail_df, width=None, height=None)
                    else:
                        st.subheader(f"{' '.join(num2words(detail_df.shape[0]).split('-')).capitalize()} flights are available  on {month_dict[user_inp['Date_of_Journey'].month]} {user_inp['Date_of_Journey'].day}, {user_inp['Date_of_Journey'].year}")
                        st.dataframe(data=detail_df, width=None, height=None)
                        if detail_df.shape[0]>11:
                            st.text("Scroll down to see all the available flights")
        with center_line:
            st.write("#")
        with right_col:
            st.write("#")
            st_lottie(flight_details_animation, speed=1.5, reverse= False, loop= True, quality='high')

############################# END: Adding Submitted resultes in a separate container ################################
st.write("---")
website_icon = Image.open("static/img/icon_website.png")
email_icon = Image.open("static/img/icon_gmail.png")
linkedin_icon = Image.open("static/img/icon_linkedin.png")
with st.container():
    st.header("Contact")
    st.write("#")
    main_col, ani_col = st.columns([3, 1])

    with main_col:
        st.write(":globe_with_meridians:  https://sai-srinivas.herokuapp.com/")
        st.write(":e-mail:  saisrinivas.samoju@gmail.com")
        st.write(":speech_balloon:  https://www.linkedin.com/in/sai-srinivas-samoju/")

    with ani_col:
        st_lottie(contact_animation, speed=1, reverse= False, loop= True, quality='high', height=125)
st.write('---')
st.text("Created by Sai Srinivas Ⓒ 2022")
