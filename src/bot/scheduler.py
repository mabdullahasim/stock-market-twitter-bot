import tweepy
from utils.format_tweet import format_preMarket_tweet
from bot.twitter_client import get_client
from datetime import datetime
from bot.data_fetching import (
    get_earnings_calendar,
    get_preMarket_losers,
    get_preMarket_gainers,
    get_economic_holiday
)
def checkTime():
    now = datetime.now()
    current_time = now.time()
    return current_time

def pre_market_gainers_tweet():
    client = get_client()
    holiday = get_economic_holiday()
    if holiday is not None:
        tweet_text = f"Today is {holiday} so market is closed"
    else:
        gainers = get_preMarket_gainers()
        tweet_text = "Pre-Market Gainers:\n" + "\n"
        tweet_text += format_preMarket_tweet(gainers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)
    
def pre_market_losers_tweet():
    client = get_client()
    holiday = get_economic_holiday()
    if holiday is not None:
        tweet_text = f"Today is {holiday} so market is closed"
    else:
        losers = get_preMarket_losers()
        tweet_text = "Pre-Market Losers:\n" + "\n"
        tweet_text += format_preMarket_tweet(losers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def earnings_tweet():
    client = getClient()
    earnings = get_earnings_calendar()
    tweet_text = format_earnings_tweet(earnings)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

if __name__ == "__main__":
    












