import requests
import bs4
import datetime

def get_flight_status(flight_code, datetime_obj):
    airline_code = flight_code.upper()[:2]
    flight_number = flight_code.upper()[2:]
    year = datetime_obj.year
    month = datetime_obj.month
    date = datetime_obj.day

    try:
        res = requests.get(f"https://www.flightstats.com/v2/flight-tracker/{airline_code}/{flight_number}?year={year}&month={month}&date={date}")
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        flight_no = soup.find("div", class_="text-helper__TextHelper-sc-8bko4a-0 OvgJa").get_text()
        flight_name = soup.find("div", class_="text-helper__TextHelper-sc-8bko4a-0 eOUwOd").get_text()

        from_code = soup.find_all("a", class_="route-with-plane__AirportLink-sc-154xj1h-3 kCdJkI")[0].get_text()
        to_code = soup.find_all("a", class_="route-with-plane__AirportLink-sc-154xj1h-3 kCdJkI")[1].get_text()

        source_city = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 Yjlkn")[0].get_text()
        destination_city = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 Yjlkn")[1].get_text()

        source = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 efwouT")[0].get_text()
        destination = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 efwouT")[1].get_text()

        source_airport = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 cHdMkI")[0].get_text()
        destination_airport = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 cHdMkI")[1].get_text()

        sch_dep_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[0].get_text()
        est_dep_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[1].get_text()
        sch_arr_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[2].get_text()
        est_arr_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[3].get_text()

        dep_terminal = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[0].get_text()
        dep_gate = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[1].get_text()
        arr_terminal = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[2].get_text()
        arr_gate = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[3].get_text()

        status = soup.find("div", class_="text-helper__TextHelper-sc-8bko4a-0 feVjck").get_text()

    except:
        try:
            res = requests.get(f"https://www.flightstats.com/v2/flight-tracker/{airline_code}*/{flight_number}?year={year}&month={month}&date={date}")
            soup = bs4.BeautifulSoup(res.text, 'html.parser')

            flight_no = soup.find("div", class_="text-helper__TextHelper-sc-8bko4a-0 OvgJa").get_text()
            flight_name = soup.find("div", class_="text-helper__TextHelper-sc-8bko4a-0 eOUwOd").get_text()

            from_code = soup.find_all("a", class_="route-with-plane__AirportLink-sc-154xj1h-3 kCdJkI")[0].get_text()
            to_code = soup.find_all("a", class_="route-with-plane__AirportLink-sc-154xj1h-3 kCdJkI")[1].get_text()

            source_city = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 Yjlkn")[0].get_text()
            destination_city = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 Yjlkn")[1].get_text()

            source = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 efwouT")[0].get_text()
            destination = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 efwouT")[1].get_text()

            source_airport = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 cHdMkI")[0].get_text()
            destination_airport = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 cHdMkI")[1].get_text()

            sch_dep_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[0].get_text()
            est_dep_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[1].get_text()
            sch_arr_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[2].get_text()
            est_arr_time = soup.find_all("div", class_="text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[3].get_text()

            dep_terminal = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[0].get_text()
            dep_gate = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[1].get_text()
            arr_terminal = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[2].get_text()
            arr_gate = soup.find_all("div", class_="ticket__TGBValue-sc-1rrbl5o-16 hUgYLc text-helper__TextHelper-sc-8bko4a-0 kbHzdx")[3].get_text()

            status = soup.find("div", class_="text-helper__TextHelper-sc-8bko4a-0 feVjck").get_text()

        except:
            return (False, {})
    return (True, {"flight_no":flight_no, "flight_name":flight_name, "from_code":from_code, "to_code":to_code,
                   "source_city":source_city, "destination_city":destination_city, "source":source,
                   "destination": destination, "source_airport":source_airport, "destination_airport":destination_airport,
                   "sch_dep_time":sch_dep_time, "est_dep_time":est_dep_time, "sch_arr_time":sch_arr_time,
                   "est_arr_time":est_arr_time, "dep_terminal":dep_terminal, "dep_gate":dep_gate,
                   "arr_terminal":arr_terminal, "arr_gate":arr_gate, "status":status})
