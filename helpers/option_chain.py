import requests
import pandas as pd

def fetch_option_chain(symbol="RELIANCE"):
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol.upper()}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.nseindia.com/option-chain"
    }

    session = requests.Session()
    session.headers.update(headers)
    session.get("https://www.nseindia.com")  # Set cookie

    response = session.get(url)
    data = response.json()

    ce_data = []
    for item in data['records']['data']:
        if 'CE' in item:
            ce_data.append(item['CE'])

    df = pd.DataFrame(ce_data)
    return df[['strikePrice', 'openInterest', 'changeinOpenInterest', 'lastPrice']]
