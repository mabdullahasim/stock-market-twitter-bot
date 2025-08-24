
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