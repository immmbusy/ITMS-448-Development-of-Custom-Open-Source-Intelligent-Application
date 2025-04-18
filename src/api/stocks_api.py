import requests
import pandas as pd

STOCK_API_KEY = "N1SGCNX71B12KFC2"

def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={STOCK_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Error Message" in data:
        raise Exception("Invalid stock symbol!")

    time_series = data.get("Time Series (Daily)", {})
    if not time_series:
        raise Exception("No data available!")

    df = pd.DataFrame(time_series).T
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    
    return df.astype(float)
