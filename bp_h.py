import requests
import json
from datetime import datetime
import time
import yfinance as yf

while True:
    # URL for Bitcoin price
    ticker_symbol = "BTC-USD"

    # Create a Ticker object
    bitcoin_ticker = yf.Ticker(ticker_symbol)

    # Get historical market data
    bitcoin_data = bitcoin_ticker.history(period="1d")

    # Print the latest closing price
    latest_price = bitcoin_data['Close'].iloc[-1]
    print(f"The latest Bitcoin price is: ${latest_price:.2f}")

    # Extract Bitcoin price in USD
    bitcoin_price_usd = float(latest_price)

    # Get the current time
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Read existing content from the file
    with open("bitcoin_prices_15.txt", "r") as file:
        lines = file.readlines()

    # Check if the number of lines exceeds 1000
    if len(lines) > 60:
        # Remove the first line
        lines.pop(0)

    # Append the new data to the list of lines
    lines.append(f"{current_time},{bitcoin_price_usd}\n")

    # Write the updated content back to the file
    with open("bitcoin_prices_15.txt", "w") as file:
        file.writelines(lines)

    # Sleep for 60 seconds before the next iteration
    time.sleep(61)
