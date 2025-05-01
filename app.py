import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Smart Money Tracker", layout="wide")
st.title("📈 Smart Money Tracker - India Edition")

tabs = st.tabs(["Smart Money Signals", "Option Chain", "Bulk Deals", "FII/DII Activity"])

with tabs[0]:
    st.header("🔍 Smart Money Signals")
    st.write("This section will show volume + delivery % spikes for Nifty stocks.")
    st.info("Feature under development")

with tabs[1]:
    st.header("📊 Option Chain")
    symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE)")
    if symbol:
        try:
            url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol.upper()}"
            headers = {"User-Agent": "Mozilla/5.0"}
            with requests.Session() as s:
                s.headers.update(headers)
                s.get("https://www.nseindia.com")  # Initialize cookies
                r = s.get(url)
            data = r.json()
            ce_data = data['records']['data']
            call_options = []
            put_options = []

            for entry in ce_data:
                if 'CE' in entry:
                    call_options.append(entry['CE'])
                if 'PE' in entry:
                    put_options.append(entry['PE'])

            ce_df = pd.DataFrame(call_options)
            pe_df = pd.DataFrame(put_options)

            st.subheader("Call Options (CE)")
            st.dataframe(ce_df)

            st.subheader("Put Options (PE)")
            st.dataframe(pe_df)

        except Exception as e:
            st.error(f"Failed to fetch option chain: {e}")

with tabs[2]:
    st.header("📦 NSE Bulk Deals")
    try:
        url = "https://www.moneycontrol.com/stocks/marketstats/bulk-deals/nse"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.content, "html.parser")
        tables = pd.read_html(r.text)
        bulk_table = tables[0]
        st.dataframe(bulk_table.head())
    except Exception as e:
        st.error(f"Failed to load bulk deals: {e}")

with tabs[3]:
    st.header("🏦 FII/DII Activity")
    try:
        url = "https://www.moneycontrol.com/stocks/marketstats/fii_dii_activity/index.php"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        tables = pd.read_html(r.text)
        fii_dii_table = tables[0]
        st.dataframe(fii_dii_table.head())
    except Exception as e:
        st.error(f"Failed to load FII/DII data: {e}")
