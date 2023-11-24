import requests

# URL to call
url = "https://www.gkenetic.com/gkenetic/?model=btc_h"

# Make the GET request
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the content of the response
    content = response.text

    # Split the content by space
    content_list = content.split()

    # Get the last second-to-last number and convert it to float
    try:
        second_to_last_number = float(content_list[-2])
        print("Last second-to-last number:", second_to_last_number)
    except ValueError:
        print("Error: Unable to convert the last second-to-last number to float")
else:
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
