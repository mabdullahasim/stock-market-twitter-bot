import pandas as pd
def format_gainers_tweet(gainers, holiday):
    lines = []
    for ticker, change, volume in gainers:
        lines.append(f"${ticker}: {change:.2f}% (Volume: {volume})")
    
    if not holiday == 'None':
        lines.append("\n" + f"Today is {holiday} so market is closed")

    tweet_text = "Top Pre-Market Gainers:\n" + "\n".join(lines)
    
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

def format_earnings(data):
    columns = [
        "logoid", "Ticker", "market_cap_basic",
        "earnings_per_share_forecast_next_fq", "earnings_per_share_fq",
        "eps_surprise_fq", "eps_surprise_percent_fq",
        "revenue_forecast_next_fq", "revenue_fq",
        "earnings_release_next_date", "earnings_release_next_calendar_date",
        "earnings_release_next_time", "description", "type", "subtype",
        "update_mode", "earnings_per_share_forecast_fq", "revenue_forecast_fq",
        "earnings_release_date", "earnings_release_calendar_date", "earnings_release_time",
        "currency", "fundamental_currency_code"
    ]

    rows = [item['d'] for item in data['data']]
    df = pd.DataFrame(rows, columns=columns)


    # Format nicely
    df['EPS est'] = df['earnings_per_share_forecast_next_fq'].apply(lambda x: f"${x:.2f}" if x else "N/A")
    df['Revenue est'] = df['revenue_forecast_next_fq'].apply(lambda x: f"${x/1e9:.2f}B" if x else "N/A")
    df['Market Cap'] = df['market_cap_basic'].apply(lambda x: f"${x/1e9:.2f}B" if x else "N/A")

    df = df[['Ticker', 'Market Cap', 'EPS est', 'Revenue est']]
    return df

