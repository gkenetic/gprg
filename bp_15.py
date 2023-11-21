import requests
import json
from datetime import datetime
import time

while True:
    # URL for Bitcoin price
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"

    # Make the HTTP request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract Bitcoin price in USD
        bitcoin_price_usd = float(data["bpi"]["USD"]["rate"].replace(',', ''))

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
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    # Sleep for 60 seconds before the next iteration
    time.sleep(61)
