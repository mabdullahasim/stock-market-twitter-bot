import tweepy
from config.twitter_client import get_client
from datetime import datetime
from config.data_fetching import (
    get_earnings_calendar,
    get_market_losers,
    get_market_gainers,
    get_economic_holiday,
    get_market_news,
    large_cap_stock_data
)
from utils.format_tweet import (
    format_preMarket_tweet,
    format_large_cap,
    format_earnings_tweet,
    format_news
)
def market_closed_tweet():
    client = get_client()
    holiday = get_economic_holiday()
    if holiday is not None:
        tweet_text = "Today is the market is closed"

    try:
        client.create_tweet(text=tweet_text)
        logger.info("Market closed tweet sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send market closed tweet: {e}")

def pre_market_gainers_tweet():
    client = get_client()
    gainers = get_market_gainers()
    tweet_text = "Pre-Market Gainers:\n" + "\n"
    tweet_text += format_preMarket_tweet(gainers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)
    
def pre_market_losers_tweet():
    client = get_client()
    losers = get_market_losers()
    tweet_text = "Pre-Market Losers:\n" + "\n"
    tweet_text += format_preMarket_tweet(losers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def after_market_gainers_tweet():
    client = get_client()
    gainers = get_market_gainers()
    tweet_text = "After-Market Gainers:\n" + "\n"
    tweet_text += format_preMarket_tweet(gainers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)
    
def after_market_losers_tweet():
    client = get_client()
    losers = get_market_losers()
    tweet_text = "After-Market Losers:\n" + "\n"
    tweet_text += format_preMarket_tweet(losers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def large_cap_stock_tweet():
    client = get_client()
    large_cap_tweet = large_cap_stock_data()
    tweet_text = format_large_cap
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def earnings_tweet():
    client = get_client()
    earnings = get_earnings_calendar()
    tweet_text = format_earnings_tweet(earnings)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def market_news_tweet():
    client = get_client()
    news = get_market_news()
    tweet_text = format_news(news)
    print(tweet_text)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

if __name__ == "__main__":
    get_market_news()
    earnings_tweet()














