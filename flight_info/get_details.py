import pandas as pd
import requests
import bs4
import datetime

def get_flight_details_input(user_inp):
    airline_code_dict = {'IndiGo': "6E", 'Air India': "AI", 'Jet Airways': "QJ", 'SpiceJet': "SG",
           'Multiple carriers': "SNC", 'GoAir': "G8", 'Vistara': "UK*", 'Air Asia': "AK",
           'Vistara Premium economy': "UK*", 'Jet Airways Business': "9W",
           'Multiple carriers Premium economy': "SNC", 'Trujet': "TRJ"}

    airport_code_dict = {'Banglore': "BLR", 'Kolkata': "CCU", 'Delhi': "DEL", 'Chennai': "MAA",
                         'Mumbai': "BOM",'New Delhi': "DEL", 'Cochin': "COK", 'Hyderabad': "HYD"}

    # from_code
    from_code = airport_code_dict[user_inp["Source"]]
    print("from code: ",from_code)

    # to_code
    to_code = airport_code_dict[user_inp["Destination"]]
    print("to code:",to_code)

    # airline_code
    if user_inp["flights"]=='All Available Airline Services':
        airline_code = None
    else:
        airline_code = airline_code_dict[user_inp["Airline"]]

    print("airline code:", airline_code)

    # datetime_obj
    datetime_obj = user_inp["Date_of_Journey"]
    print("datetime obj:",datetime_obj)

    return from_code, to_code, airline_code, datetime_obj

def get_flight_details(from_code, to_code, airline_code=None, datetime_obj=datetime.date.today()):

    df = pd.DataFrame(columns = ["Flight Number", "Flight Name", "Departure Time", "Arrival Time"])

    # Input data
    # from_code = "BLR"
    # to_code = "VTZ"
    # airline_code = "6E"
    # airline_code = None
    year = datetime_obj.year
    month = datetime_obj.month
    date = datetime_obj.day
    hours = [0, 6, 12, 18]

    if airline_code:
        # Single Service
        for hour in hours:
            try:
                url = f"https://www.flightstats.com/v2/flight-tracker/route/{from_code}/{to_code}/{airline_code}?year={year}&month={month}&date={date}&hour={hour}"
                print(url)
                res = requests.get(url)
                soup = bs4.BeautifulSoup(res.text, 'html.parser')
                details_raw = soup.find_all("h2", class_="table__CellText-sc-1x7nv9w-15 fcTUax")
                for i in range(len(details_raw)//3):
                    try:
                        flight_number = details_raw[0+i*3].get_text()
                        dep_time = details_raw[1+i*3].get_text()
                        arr_time = details_raw[2+i*3].get_text()
                        flight_name = soup.find_all("span", class_="table__SubText-sc-1x7nv9w-16 bQPdJx")[i*2].get_text()
                        df.loc[len(df.index)] = [flight_number, flight_name, dep_time, arr_time]
                    except:
                        print("Single airline service")
                        print(f"Error in the inner exception block for i={i} and hour={hour}")
            except:
                print("Single airline service")
                print(f"Error in the outer exception block for hour={hour}")
                continue
    else:
        # All services
        for hour in hours:
            try:
                url = f"https://www.flightstats.com/v2/flight-tracker/route/{from_code}/{to_code}/?year={year}&month={month}&date={date}&hour={hour}"
                print(url)
                res = requests.get(url)
                soup = bs4.BeautifulSoup(res.text, 'html.parser')
                full_table = soup.find_all("div", class_="table__Table-sc-1x7nv9w-6 zGTLC")[0]
                for i in range(len(full_table)-1):
                    try:
                        items = full_table.find_all("a", class_="table__A-sc-1x7nv9w-2 hnJChl")[i].find_all("h2", class_="table__CellText-sc-1x7nv9w-15 fcTUax")
                        flight_number = items[0].get_text()
                        dep_time = items[1].get_text()
                        arr_time = items[2].get_text()
                        flight_name = full_table.find_all("span", class_="table__SubText-sc-1x7nv9w-16 bQPdJx")[i*2].get_text()
                        df.loc[len(df.index)] = [flight_number, flight_name, dep_time, arr_time]
                    except:
                        print("All airline services")
                        print(f"Error in the inner exception block for i={i} and hour={hour}")
            except:
                print("All airline services")
                print(f"Error in the outer exception block for hour={hour}")

    return df
