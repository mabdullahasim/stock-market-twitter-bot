import pandas as pd
from openai import OpenAI
from utils.format_data import format_earnings
from datetime import datetime
import os
from dotenv import load_dotenv
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

def format_news(news):
    lines = []
    summary = clean_market_news(news["summary"])
    lines.append(summary +"\n")
    lines.append("Source: "+news["source"]+"\n")
    lines.append(news["url"]+"\n")
    tweet_text = f'{news["title"]}:\n' + "\n".join(lines)
    return tweet_text

def clean_market_news(summary):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
        Clean this market summary
        
        Rules:
        - If the text is already good just return a short clean version
        - If it has filler like "transcripts from earnings call" or "brought to you by Benzinga APIs", remove that.
        - I want clean small summary no useless info
        - If the summary is to vauge give it some depth, keep it short and relevant
        - Do not add fluff or make it long.

        Example input:
        Webull Corp BULL reported its second-quarter financial results after the market close on Thursday.
        Below are the transcripts from the second quarter earnings call. This transcript is brought to you by Benzinga APIs.
        For real-time access to our entire catalog, please visit ...

        Expected output:
        Webull Corp BULL reported its second-quarter financial results after the market close on Thursday.

        {summary}
        """

    response = client.chat.completions.create(
        model ="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()