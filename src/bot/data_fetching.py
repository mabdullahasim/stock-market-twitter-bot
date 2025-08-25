import yfinance as yf
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from utils.format_tweet import format_gainers_tweet
from utils.format_tweet import format_earnings_tweet
import pandas as pd
import time
from datetime import datetime, timedelta


load_dotenv()
def get_preMarket_data():
    PRE_MARKET_URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/"
    gainers = []
    response = requests.get(PRE_MARKET_URL)         #sends http request to the pre_market_url gets full html content of page
    html = response.text                            #extracts the text content of the page, contains all of the <html> <body> etc
    soup = BeautifulSoup(html, "html.parser")       #creates a beautiful soup object called soup that lets u parse the html content
    tbody = soup.find("tbody")                      #finds the <tbody> elemt on the page
    rows = tbody.find_all("tr")                     #gets all the <tr> tags in the <tbody> each tr is one stocks row
    top_rows = rows[:5]                             #gets the top 5 tickers
    for row in top_rows:                                #iterates throughj each row in the table
        cells = row.find_all("td")                  #finds all the td elements in the row
        ticker = cells[0].find("a").text.strip()    #inside the first td it finds the a element which contains the ticker
        percent_change = cells[1].text.strip()      #inside the seccond td it finds the percent change
        pre_market_volume = cells[4].text.strip()   #inside the fourth td it finds the pre-market volume
        percent_change = float(percent_change.replace("%","")) # convert the sstring number into a float
        gainers.append((ticker, percent_change, pre_market_volume)) #add the gainers to the list
    return gainers

def large_cap_stock_data():
    tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "META", "PLTR", "AMD", "AMZN"]  #large cap tickers to get data from
    gainers = []                                                               #temp list
    for ticker in tickers:                                                     #iterate through the tickers in tickers
        stock = yf.Ticker(ticker)                                              #create a stock object for the specified ticker
        data = stock.history(period="2d")                                      #get the data for the tco from the past 2 days

        current_price = data['Close'].iloc[-1]                                  #gets the current price held in close for the day
        current_volume = data['Volume'].iloc[-1]                               #gets the current volume for the day
        yesterday_close = data['Close'].iloc[-2]                                #gets the closing price of the day before

        percent_change = ((current_price - yesterday_close) / yesterday_close) * 100   #calculate the percentage change from yesterday to current price
        gainers.append((ticker, percent_change, current_volume))                    #add the data for the stocks to gainers
    large_cap_data = sorted(gainers, key=lambda x: x[1], reverse=True)                 #store the data in large_cap_data sorted by percentage change
    return large_cap_data                                                              #return the large_cap_stock data

def get_preMarket_losers():
    PRE_MARKET_URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-losers/"
    losers = []
    response = requests.get(PRE_MARKET_URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    tbody = soup.find("tbody")
    rows = tbody.find_all("tr")
    top_rows = rows[:5]
    for row in top_rows:
        cells = row.find_all("td")
        ticker = cells[0].find("a").text.strip()
        percent_change = cells[1].text.strip()
        pre_market_volume = cells[4].text.strip()
        percent_change = percent_change.replace("+", "").replace("%", "").replace("−", "-")
        percent_change = float(percent_change)
        losers.append((ticker, percent_change, pre_market_volume))
    return losers

def get_economic_holiday():
    API_KEY = os.getenv("FIN_API_KEY")
    URL = f"https://finnhub.io/api/v1/stock/market-status?exchange=US&token={API_KEY}"
    response = requests.get(URL)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    try:
        data = response.json()
    except Exception:
        return "Error: Could not parse JSON (check API key or endpoint)."
    
    return data.get("holiday")

def get_earnings_calendar():
    url = "https://scanner.tradingview.com/america/scan?label-product=screener-stock-old" #url to get request from
    today = datetime.today() #current date and time
    start_of_week = today - timedelta(days=today.weekday()) #get the monday of the current week
    end_of_week = start_of_week + timedelta(days=6)#get the sunday of the current week
    start_ts = int(start_of_week.timestamp()) #timestamp converts date to a unix time stamp which url expects
    end_ts   = int(end_of_week.timestamp())

    payload = { #payload to be sent with the request
        "filter": [ #filter defines which stocks to return
            {"left": "is_primary", "operation": "equal", "right": True},
            {"left": "earnings_release_date,earnings_release_next_date", "operation": "in_range", "right": [start_ts, end_ts]}, #only want earnings releases between start_ts and end_ts
            {"left": "earnings_release_date,earnings_release_next_date", "operation": "nequal", "right": end_ts}
        ],
        "options": {"lang": "en"},
        "markets": ["america"],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": [ #columns tells the url which feilds you want
            "name",
            "earnings_per_share_forecast_fq", "revenue_forecast_fq",
            "earnings_release_calendar_date"
        ],
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}, #sort sorts by basic market cap
        "preset": None,
        "range": [0,4] #returns rows from 0 to 5
    }

    headers = { #headers tells the url that you are sending json in the post request
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers) #sends pay load to the url
    data = response.json() #parse the response
    tweet = format_earnings_tweet(data) #send the data to a formmater
    print(tweet)


if __name__ == "__main__":
    calendar = get_earnings_calendar()
    