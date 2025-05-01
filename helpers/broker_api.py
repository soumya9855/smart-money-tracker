from kiteconnect import KiteConnect

# Fill in your API Key/Secret
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_saved_access_token"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

def get_holdings():
    try:
        return kite.holdings()
    except Exception as e:
        print("Error fetching holdings:", e)
        return []
