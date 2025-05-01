import pandas as pd
from helpers.option_chain import fetch_option_chain
from helpers.bulk_deals import fetch_bulk_deals
from datetime import datetime


# Fetch Option Chain Data (Open Interest + Price Divergence)
def analyze_option_chain(symbol):
    df = fetch_option_chain(symbol)
    
    if df.empty:
        return None

    # Analyze OI change
    df['oi_change'] = df['openInterest'].diff()
    max_oi_strike = df.loc[df['oi_change'].idxmax()]
    
    # Signal: Significant Open Interest Change
    signal = ""
    if max_oi_strike['oi_change'] > 1000:  # Threshold for significant OI change
        signal = f"🚨 Option Chain Alert for {symbol.upper()}: " \
                 f"Large OI change at strike {max_oi_strike['strikePrice']} of {max_oi_strike['oi_change']} contracts."

    return signal


# Fetch Bulk Deals & Block Deals
def analyze_bulk_deals(symbol):
    df = fetch_bulk_deals()

    if df.empty:
        return None

    # Signal: Large Deals in Stock (Thresholds based on stock liquidity)
    threshold_value = 1000000  # Deals greater than 10 lakhs INR
    large_deals = df[df['Value'] > threshold_value]

    signals = []
    if not large_deals.empty:
        for _, row in large_deals.iterrows():
            signals.append(f"🚨 Large Deal Alert for {symbol.upper()}: " 
                           f"Block deal of {row['Quantity']} shares worth ₹{row['Value']}")

    return signals


# Detect Smart Money Signals
def detect_signals(symbol):
    # Analyze option chain data
    option_chain_signal = analyze_option_chain(symbol)
    
    # Analyze bulk/block deals
    bulk_deals_signals = analyze_bulk_deals(symbol)

    # Combining signals
    signals = []
    if option_chain_signal:
        signals.append({'symbol': symbol, 'type': 'Option Chain', 'message': option_chain_signal})
    
    if bulk_deals_signals:
        for msg in bulk_deals_signals:
            signals.append({'symbol': symbol, 'type': 'Bulk Deal', 'message': msg})

    # Returning signals and chart data
    chart_data = pd.DataFrame({'Date': pd.date_range(end=datetime.today(), periods=10).tolist(),
                               'Close': [2500 + i * 5 for i in range(10)],
                               'Delivery %': [10000 + i * 200 for i in range(10)]})  # Placeholder chart data
    return pd.DataFrame(signals), chart_data


