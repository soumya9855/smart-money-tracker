import pandas as pd
import requests
from datetime import datetime

def fetch_bulk_deals():
    url = "https://www.nseindia.com/api/reports?type=bdeq"
    headers = {"User-Agent": "Mozilla/5.0"}

    # NSE restricts direct API use without session cookies. Workaround: use CSV from:
    csv_url = "https://www1.nseindia.com/products/content/equities/equities/bulk.csv"
    df = pd.read_csv(csv_url)

    today = datetime.today().strftime("%d-%b-%Y").upper()
    df_today = df[df['Date'] == today]
    df_today.to_csv("data/bulk_deals_today.csv", index=False)

    return df_today
