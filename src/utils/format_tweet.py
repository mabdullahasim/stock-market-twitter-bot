import pandas as pd
from utils.format_data import format_earnings
from datetime import datetime
def format_preMarket_tweet(data):
    lines = []
    for ticker, change, volume in data:
        lines.append(f"${ticker}: {change:.2f}% (Volume: {volume})")
    tweet_text = "\n".join(lines)
    # Ensure tweet is within 280 characters
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."

    return tweet_text

def format_large_cap(large_cap):
    lines = []
    for ticker, change, volume in large_cap:
        lines.append(f"${ticker}: {change:.2f}% (Volume: {volume})")

    tweet_text = "Large-Cap Stock Highlights:\n" + "\n".join(lines)
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."

    return tweet_text

def format_earnings_tweet(data):
    df = format_earnings(data)
    lines = []
    for _, row in df.iterrows(): #iterate through rows in the data frame
        ticker = row['Ticker']
        eps_est = row['EPS est']
        rev_est = row['Revenue est']
        date = row['earnings_date']
        timestamp = row['earnings_date']
        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d") if pd.notna(timestamp) else "N/A"
        lines.append(f"${ticker:<5} | Eps {eps_est:<6} | Rev {rev_est:<8} | Date {date}")

    tweet_text = "Largest Cap Earning Estimates This Week:\n" + "\n".join(lines)
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277]

    return tweet_text