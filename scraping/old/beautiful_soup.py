import csv
from bs4 import BeautifulSoup
import requests

tweet_url = "https://twitter.com/sajzxa/status/1699570836532015404"

try:
    response = requests.get(tweet_url)
    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to retrieve content for URL: {tweet_url}")

except Exception as e:
    print(f"Error fetching URL: {tweet_url}")


soup = BeautifulSoup(
    html_content, "html.parser")
# Extract the tweet text
tweet_text = soup.get_text()

# Print or store the tweet text
print(tweet_text)
