import tweepy
from dotenv import load_dotenv
import os
from bot.data_fetching import get_preMarket_data
from bot.format_tweet import format_gainers_tweet

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

if __name__ == "__main__":
    gainers = get_preMarket_data()
    tweet_text = format_gainers_tweet(gainers)
    print(tweet_text)
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully! Tweet ID:", response.data['id'])
    except tweepy.TweepyException as e:
        print("Failed to post tweet:", e)