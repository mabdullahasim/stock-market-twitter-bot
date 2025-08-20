def format_gainers_tweet(gainers):
    lines = []
    for ticker, change, volume in gainers:
        lines.append(f"${ticker}: {change:.2f}% (Volume: {volume})")
    
    tweet_text = "Top Pre-Market Gainers:\n" + "\n".join(lines)
    
    # Ensure tweet is within 280 characters
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    
    return tweet_text