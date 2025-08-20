import requests
from bs4 import BeautifulSoup
PRE_MARKET_URL = "https://www.tradingview.com/markets/stocks-usa/market-movers-pre-market-gainers/"

def get_preMarket_data():
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
        percent_change = float(percent_change.replace("+","").replace("%","")) # convert the sstring number into a float
        gainers.append((ticker, percent_change, pre_market_volume)) #add the gainers to the list
    return gainers



def format_gainers_tweet(gainers):
    lines = []
    for ticker, change, volume in gainers:
        lines.append(f"{ticker}: {change:.2f}% (Volume: {volume})")
    return "\n".join(lines)

if __name__ == "__main__":
    gainers = get_preMarket_data()
    print("Top pre-market Gainers:")
    text_tweet = format_gainers_tweet(gainers)
    print(text_tweet)