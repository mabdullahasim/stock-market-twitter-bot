import tweepy
from bot.data_fetching import get_preMarket_data
from bot.format_tweet import format_gainers_tweets
from bot.twitter_client import getClient
from datetime import datetime

def checkTime():
    now = datetime.now()
    current_time = now.time()
    return current_time


def pre_market_tweet():
    client = getClient():
    gainers = get_preMarket_data()
    tweet_text = format_gainers_tweet(gainers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)

def after_hours_tweet():
    client = getClient():
    gainers = get_preMarket_data()
    tweet_text = format_gainers_tweet(gainers)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)
















