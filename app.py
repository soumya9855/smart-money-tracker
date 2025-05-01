import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Set up the page title and layout
st.set_page_config(page_title="Smart Money Tracker", layout="wide")
st.title("📈 Smart Money Tracker - India Edition")

# Define the tabs in Streamlit
tabs = st.tabs(["Smart Money Signals", "Option Chain", "Bulk Deals", "FII/DII Activity"])

# Smart Money Signals Tab
with tabs[0]:
    st.header("🔍 Smart Money Signals")
    st.write("This section will show volume + delivery % spikes for Nifty stocks.")
    st.info("Feature under development")  # Placeholder for future functionality

# Option Chain Tab
with tabs[1]:
    st.header("📊 Option Chain")
    symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE)")
    
    if symbol:
        try:
            url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol.upper()}"
            headers = {"User-Agent": "Mozilla/5.0"}
            
            # Session for handling cookies
            with requests.Session() as s:
                s.headers.update(headers)
                s.get("https://www.nseindia.com")  # Initialize cookies
                r = s.get(url)
            
            data = r.json()
            ce_data = data['records']['data']
            call_options = []
            put_options = []

            # Parse call and put options
            for entry in ce_data:
                if 'CE' in entry:
                    call_options.append(entry['CE'])
                if 'PE' in entry:
                    put_options.append(entry['PE'])

            # Convert to DataFrame and display
            ce_df = pd.DataFrame(call_options)
            pe_df = pd.DataFrame(put_options)

            st.subheader("Call Options (CE)")
            st.dataframe(ce_df)

            st.subheader("Put Options (PE)")
            st.dataframe(pe_df)

        except Exception as e:
            st.error(f"Failed to fetch option chain: {e}")

# NSE Bulk Deals Tab
with tabs[2]:
    st.header("📦 NSE Bulk Deals")
    try:
        # Fetch the bulk deals data from MoneyControl
        url = "https://www.moneycontrol.com/stocks/marketstats/bulk-deals/nse"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.content, "html.parser")

        # Parse the bulk deals table
        tables = pd.read_html(r.text)

        # If tables are found, show the first one
        if tables:
            bulk_table = tables[0]
            st.dataframe(bulk_table.head())
        else:
            st.warning("No bulk deals data found.")

    except Exception as e:
        st.error(f"Failed to load bulk deals: {e}")

# FII/DII Activity Tab
with tabs[3]:
    st.header("🏦 FII/DII Activity")
    try:
        # Fetch FII/DII data from MoneyControl
        url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        tables = pd.read_html(r.text)

        # If tables are found, display the first one
        if tables:
            fii_dii_table = tables[0]
            st.dataframe(fii_dii_table.head())
        else:
            st.warning("No FII/DII activity data found.")
            
    except Exception as e:
        st.error(f"Failed to load FII/DII data: {e}")
