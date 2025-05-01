import schedule
import time
from helpers.signal_logic import detect_signals
from helpers.alert_bot import send_telegram_alert

def scheduled_task():
    symbols = ["RELIANCE", "HDFCBANK", "TCS"]
    for sym in symbols:
        signals, _ = detect_signals(sym)
        for msg in signals['message']:
            send_telegram_alert(msg)

# Run daily at 15:15 (End-of-day analysis)
schedule.every().day.at("15:15").do(scheduled_task)

while True:
    schedule.run_pending()  # Execute all scheduled tasks
    time.sleep(60)  # Wait for 60 seconds before checking again

