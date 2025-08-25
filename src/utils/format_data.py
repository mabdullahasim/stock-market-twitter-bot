import pandas as pd
def format_earnings(data):
    columns = [
        "Ticker",
        "eps_fq", "rev_fq",
        "earnings_date"
    ]

    rows = [item['d'] for item in data['data']]
    df = pd.DataFrame(rows, columns=columns)


    # Format nicely
    df['EPS est'] = df['eps_fq'].apply(lambda x: f"${x:.2f}" if x else "N/A")
    df['Revenue est'] = df['rev_fq'].apply(lambda x: f"${x/1e9:.2f}B" if x else "N/A")

    df = df[['Ticker', 'EPS est', 'Revenue est', 'earnings_date']]
    return df