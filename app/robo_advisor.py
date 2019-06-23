# app/robo_advisor.py

import csv
import json
import os
import datetime

from dotenv import load_dotenv
import requests

load_dotenv() #> to load contents of the .env file into the script's environment

api_key =os.environ.get("ALPHAVANTAGE_API_KEY") # to obtain API_KEY from env file. 

def to_usd(my_price):
    return "${0:,.2f}".format(my_price) #> 12,000.71

def get_response(symbol):  #> To define and return the result after user input. 
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    #print(response.status_code) #> 200

    try:
        parsed_response["Time Series (Daily)"]
    except: #> "OOPS" will generate below error message
        print("-------------------------")
        print("ERROR MESSAGE:")
        print("SORRY. WE COULD NOT FIND ANY TRADING DATA FOR THE ENTERED STOCK SYMBOL.\n"+
        "PLEASE CHECK THE SYMBOL AND TRY IT AGAIN")
        exit()

    return parsed_response

if __name__ == "__main__":

    # INPUTS

    symbol = input("Please input a stock symbol (e.g. MSFT) and press enter: ") # Asking for user input of stock symbol

    if not symbol.isalpha():  # PRELIM VALIDATION for non-letter inputs. #source: https://stackoverflow.com/questions/30994738/how-to-make-input-only-accept-a-z-etc
        print("-------------------------")
        print("ERROR MESSAGE:")
        print("OH, PLEASE ONLY USE THE LETTER(S) FOR YOUR INPUT (e.g. MSFT). PLEASE TRY AGAIN.")
        exit()
    elif len(symbol) > 6: # PRELIM VALIDATION for limiting the number of letters equal to or less than 6. # Source: https://stackoverflow.com/questions/8761778/limiting-python-input-strings-to-certain-characters-and-lengths
        print("-------------------------")
        print("ERROR MESSAGE:")
        print("OH, EXPECTING PROPERLY-FORMED STOCK SYMBOL LIKE 'MSFT'. PLEASE TRY AGAIN.")
        exit()
    else:
        parsed_response = get_response(symbol)  # When valid input is entered. 

        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

        tsd = parsed_response["Time Series (Daily)"]

        dates = list(tsd.keys()) 
        latest_day = dates[0] 

        latest_close = tsd[latest_day]["4. close"]

        high_prices = []
        low_prices = []

        for date in dates:
            high_price = tsd[date]["2. high"]
            low_price = tsd[date]["3. low"]
            high_prices.append(float(high_price))
            low_prices.append(float(low_price))

        recent_high = max(high_prices)
        recent_low = min(low_prices)

       # OUTPUTS

        file_name = symbol +".csv"
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices_" + file_name)

        csv_headers = ["timestamp", " open", " high", " low", " close", " volume"]

        with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader() # uses fieldnames set above
            for date in dates:
                daily_prices = tsd[date]
                writer.writerow({
                    "timestamp": date,
                    " open": daily_prices["1. open"],
                    " high": daily_prices["2. high"],
                    " low": daily_prices["3. low"],
                    " close": daily_prices["4. close"],
                    " volume": daily_prices["5. volume"]
                })

        # FORMATTING FOR DISPLAYING RESULT

        current_time = datetime.datetime.now()  #> current time

        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  #>'2019-06-21 14:00:00' (reference: from prior class discussion)

        # RECOMMENDATION CALCULATION

        average_price = (recent_high + recent_low)/2 #> Calculate the mean of recent high and recent low as a basis
        my_target_price = average_price*0.9 #> My target price is 10% discount (or 0.9 times) from the average_price due to the recent market uncertainty. If my target price is above latest close price, it is a BUY. If not, it is DO NOT BUY.

        # DISPLAYTING RESULT

        print("-------------------------")
        print(f"YOUR SELECTED SYMBOL: {symbol}")
        print("-------------------------")
        print(f"REQUEST AT: {formatted_current_time}")
        print(f"LAST REFRESH DATE: {last_refreshed}")
        print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
        print(f"RECENT HIGH: {to_usd(float(recent_high))}")
        print(f"RECENT LOW: {to_usd(float(recent_low))}")
        print("-------------------------")

        if str(my_target_price) > latest_close: #>BUY RATING (example: try Walmart "WMT" )
            print("RECOMMENDATION: BUY")
        elif str(my_target_price) < latest_close: #>SELL RATING (example: try Apple "AAPL" )
            print("RECOMMENDATION: DO NOT BUY")

        if str(my_target_price) > latest_close: #> EXPLANATION FOR BUY RATING
            print(f"RECOMMENDATION REASON: OUR TARGET PRICE IS BASED UPON THE MEAN OF RECENT HIGH\n"+ 
            "AND RECENT LOW MINUS 10% DISCOUNT DUE TO THE RECENT MARKET VOLATILITY,\n"+ 
            "PRIMARILY RESULTED BY THE UNCERTAINY ON THE TRADE WAR AND OTHER GEOGRAPHICAL TENSIONS.\n"+
            "ALTHOUGH WE BELIEVE THAT THE MARKET WILL BECOME BEARISH TOWARD THE END OF THE YEAR,\n"+       
            "OUR TARGET PRICE IS HIGHER THAN THE LATEST CLOSE PRICE. THEREFORE, WE RECOMMEND A 'BUY' RATING.")

        elif str(my_target_price) < latest_close: #> EXPLANATION FOR DO NOT BUY RATING
            print(f"RECOMMENDATION REASON: OUR TARGET PRICE IS BASED UPON THE MEAN OF RECENT HIGH\n"+ 
            "AND RECENT LOW MINUS 10% DISCOUNT DUE TO THE RECENT MARKET VOLATILITY,\n"+ 
            "PRIMARILY RESULTED BY THE UNCERTAINY ON THE TRADE WAR AND OTHER GEOGRAPHICAL TENSIONS.\n"+
            "WE BELIEVE THAT THE MARKET WILL BECOME BEARISH TOWARD THE END OF THE YEAR, AND\n"+     
            "OUR TARGET PRICE IS LOWER THAN THE LATEST CLOSE PRICE. THEREFORE, WE RECOMMEND A 'DO NOT BUY' RATING.")

        print("-------------------------")
        print(f"WRITING DATA TO CSV IN THE FOLLOWING PATH: {csv_file_path}...")
        print("YOUR OUTPUT TO CSV FILE IS NOW COMPLETE")
        print("-------------------------")
        print("HAPPY INVESTING!")
        print("-------------------------")
        
