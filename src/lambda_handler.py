import logging
from config.scheduler import (
    pre_market_gainers_tweet,
    pre_market_losers_tweet,
    after_market_gainers_tweet,
    after_market_losers_tweet,
    earnings_tweet,
    market_news_tweet,
    large_cap_stock_tweet,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    job = event.get("job")
    logger.info(f"Running job: {job}")
    closed_message = get_market_status_message()
    if closed_message:
        logger.info("Market is closed. Sending closed-market tweet.")
        market_closed_tweet(closed_message)
        return {"statusCode": 200, "body": "Market closed, tweeted message."}
        
    if job == "pre_market_gainers":
        pre_market_gainers_tweet()
    elif job == "pre_market_losers":
        pre_market_losers_tweet()
    elif job == "after_market_gainers":
        after_market_gainers_tweet()
    elif job == "after_market_losers":
        after_market_losers_tweet()
    elif job == "large_cap_tweet":
        large_cap_stock_tweet()
    elif job == "earnings":
        earnings_tweet()
    elif job == "market_news":
        market_news_tweet()
    else:
        logger.error(f"Unknown job: {job}")
        return {"statusCode": 400, "body": f"Unknown job {job}"}

    return {"statusCode": 200, "body": f"Successfully ran {job}"}