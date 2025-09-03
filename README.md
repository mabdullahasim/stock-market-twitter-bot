Stock Market Twitter Bot:

    A Python bot that automatically posts financial and stock market updates on Twitter.
    It provides key market information at market open, mid-day,
    and close, keeping followers informed about top gainers,
    losers, trading volume, and major news.

Features:

    Pre-market gainers: Highlights the top-performing stocks before market open.

    Mid-day updates: Covers stocks making significant moves during regular trading hours.

    Market close summary: Lists the biggest gainers, losers, and overall market highlights.

    News integration: Posts relevant financial news affecting the markets.

    Earings updates: Posts earnigns updates for the week

    AI usage: Uses openAI's chat gpt to summarize a news article given rules

Tech Stack:
    Python 3

    Tweepy (or other Twitter API library for posting tweets)

    Requests / BeautifulSoup (for market data scraping)

    dotenv (for environment variables and API keys)

    OpenAI API (for summarizing or formatting news, if used)

    Pandas & NumPy (for data manipulation)

    YFinance (for stock market data)

    AWS Lambda (for serverless deployment)

Setup Instructions:
1. Clone the repository:
    git clone <your-repo-url>
    cd stock-market-twitter-bot

2. Create a virtual enviorment(optional):
    python3 -m venv venv
    source venv/bin/activate

3. Install dependencies:
    pip install -r requirements.txt

4. Set up environment variables:
    create a .env file in the project root.
    TWITTER_API_KEY=your_api_key
    TWITTER_API_SECRET_KEY=your_api_secret
    TWITTER_ACCESS_TOKEN=your_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

5. Configure bot settings:
    You can customize posting times, stock tickers, or news sources in the configuration file.

License:
    This project is licensed under the MIT License.
