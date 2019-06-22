# app/robo_advisor.py

import csv
import json
import os
import datetime

from dotenv import load_dotenv
import requests

load_dotenv() #> to load contents of the .env file into the script's environment

# utility function to convert float or integer to usd-formatted string (for printing)

def to_usd(my_price):
    return "${0:,.2f}".format(my_price) #> 12,000.71



#
# INFO INPUTS
#

api_key =os.environ.get("ALPHAVANTAGE_API_KEY") # to obtain API_KEY from env file. 


symbol = input("Please input a stock symbol (e.g. MSFT) and press enter: ") # Asking for user input of stock symbol

def returned_response(symbol):  #> To define and return the result after user input. TODO: How to integrate multiple inputs (for further challenge)
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

parsed_response = returned_response(symbol)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

#breakpoint()

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) #TODO: assumes first day is on top, but consider sorting to ensure latest day is first

latest_day = dates[0] #TODO: make the latest date dynamic

latest_close = tsd[latest_day]["4. close"]


# get high price from each day
#high_prices = [10,20,30,5]
#recent_high = max(high_prices)
# maximum of all high prices

high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

recent_high = max(high_prices)
recent_low = min(low_prices)

#
# INFO OUTPUTS
#

#csv_file_path = "data/prices.csv" # a relative filepath

file_name = symbol +".csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + file_name)

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })


# DISPLAY RESULTS

current_time = datetime.datetime.now()  #> current time

formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  #>'2019-06-21 14:00:00' (reference: from prior class discussion)

# RECOMMENDATION CALCULATION

average_price = (recent_high + recent_low)/2 #> Calculate the average of recent high and recent low as a basis
my_target_price = average_price*0.85 #> My target price is 15% premium to the average price due to the recent market strength. If my target price is above latest close price, it is a BUY. If not, it is SELL. If same, it is HOLD.


print("-------------------------")
print(f"YOUR SELECTED SYMBOL: {symbol}")
print("-------------------------")
print(f"REQUEST AT: {formatted_current_time}")
print(f"LAST REFRESH DATE: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")

if str(my_target_price) > latest_close: #>BUY RATING
    print("RECOMMENDATION: BUY")
elif str(my_target_price) < latest_close: #>SELL RATING
    print("RECOMMENDATION: SELL")
else:
    print("RECOMMENDATION: HOLD") #>HOLD RATING

if str(my_target_price) > latest_close: #> EXPLANATION FOR BUY RATING
    print(f"RECOMMENDATION REASON: OUR TARGET PRICE IS BASED UPON THE AVERAGE OF RECENT HIGH\n"+ 
    "AND RECENT LOW MINUS 15% DISCOUNT DUE TO THE RECENT MARKET VOLATILITY\n"+ 
    "PRIMARILY RESULTED BY THE UNCERTAINY ON THE TRADE WAR AND OTHER GEOGRAPHICAL TENSION WITH IRAN\n"+
    "OUR TARGET PRICE IS HIGHER THAN THE LATEST CLOSE PRICE THEREFORE, WE RECOMMEND A BUY RATING\n")
elif str(my_target_price) < latest_close: #> EXPLANATION FOR SELL RATING
    print(f"RECOMMENDATION REASON: OUR TARGET PRICE IS BASED UPON THE AVERAGE OF RECENT HIGH\n"+ 
    "AND RECENT LOW MINUS 15% DISCOUNT DUE TO THE RECENT MARKET VOLATILITY\n"+ 
    "PRIMARILY RESULTED BY THE UNCERTAINY ON THE TRADE WAR AND OTHER GEOGRAPHICAL TENSION WITH IRAN\n"+
    "OUR TARGET PRICE IS LOWER THAN THE LATEST CLOSE PRICE THEREFORE, WE RECOMMEND A SELL RATING\n")
else: #> EXPLANATION FOR HOLD RATING
    print(f"RECOMMENDATION REASON: OUR TARGET PRICE IS BASED UPON THE AVERAGE OF RECENT HIGH\n"+ 
    "AND RECENT LOW MINUS 15% DISCOUNT DUE TO THE RECENT MARKET VOLATILITY\n"+ 
    "PRIMARILY RESULTED BY THE UNCERTAINY ON THE TRADE WAR AND OTHER GEOGRAPHICAL TENSION WITH IRAN\n"+
    "OUR TARGET PRICE IS SAME THE LATEST CLOSE PRICE THEREFORE, WE RECOMMEND A HOLD RATING\n")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("YOUR OUTPUT TO CSV FILE IS COMPLETE")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


