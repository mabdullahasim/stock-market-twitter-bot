import yfinance as yf
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime

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
    status = data.get('isOpen', "unknown")
    if status == True:
        return "Market is Closed today"
    else:
        return f"Market is Open right now"
    return "Market is Open today"





def format_tweet(gainers):
    lines = []
    for ticker, change, volume in gainers:
        lines.append(f"{ticker}: {change:.2f}% (Volume: {volume})")
    return "\n".join(lines)

if __name__ == "__main__":
    # gainers = get_preMarket_data()
    # losers = get_preMarket_losers()
    # large_cap_stocks = large_cap_stock_data()
    # print("Top pre-market Gainers:")
    # text_tweet = format_tweet(gainers)
    # print(text_tweet + "\n")
    # print("Top pre-market Losers:")
    # text_tweet = format_tweet(losers)
    # print(text_tweet + "\n")
    # print("Large Cap Stock Activity:")
    # text_tweet = format_tweet(large_cap_stocks)
    # print(text_tweet)
    print(get_economic_holiday())