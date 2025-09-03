import logging
from config.scheduler import (
    pre_market_gainers_tweet,
    pre_market_losers_tweet,
    after_market_gainers_tweet,
    after_market_losers_tweet,
    earnings_tweet,
    market_news_tweet,
    large_cap_stock_tweet,
    market_closed_tweet
)
from config.data_fetching import get_economic_holiday

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    job = event.get("job")
    logger.info(f"Running job: {job}")
    holiday = get_economic_holiday()
    if holiday is not None:
        logger.info(f"Market is closed today: {holiday}")
        market_closed_tweet()
        return {"statusCode": 200, "body": f"Market is closed today: {holiday}. Tweet sent."}

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