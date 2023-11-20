import requests
import json
from datetime import datetime
import time
import yfinance as yf

def get_tesla_stock_price():
    # Define the stock symbol for Tesla
    stock_symbol = "TSLA"

    try:
        # Fetch historical market data for the specified stock symbol
        stock_data = yf.Ticker(stock_symbol)

        # Get the current stock price
        current_price = stock_data.info['ask']
        return current_price

    except Exception as e:
        print(f"Error fetching stock price: {e}")
        return None

while True:
    # URL for the Yahoo Finance VIX data
        # Extract the VIX value from the HTML response
    tsla_value = get_tesla_stock_price()

    # Get the current time
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Read existing content from the file
    with open("tsla_data_h.txt", "r") as file:
        lines = file.readlines()

    # Check if the number of lines exceeds a certain limit (e.g., 60)
    if len(lines) > 60:
        # Remove the first line
        lines.pop(0)

    # Append the new data to the list of lines
    lines.append(f"{current_time},{tsla_value}\n")

    # Write the updated content back to the file
    with open("tsla_data_h.txt", "w") as file:
        file.writelines(lines)

    # Sleep for 60 seconds before the next iteration
    time.sleep(61)
