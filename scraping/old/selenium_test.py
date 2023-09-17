import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
os.system('ls')
# Create a WebDriver instance (you need to specify the path to your driver executable)
driver = webdriver.Chrome(executable_path='./chromed/chromedriver')


def get_tweet(tweet_id):
    tweet_url = 'https://twitter.com/anyuser/status/' + tweet_id
    driver.get(tweet_url)

    # Wait for the page to load (you can adjust the waiting time as needed)
    driver.implicitly_wait(30)
    try:
        tweet_element = driver.find_element(
            By.CSS_SELECTOR, '[data-testid=\"tweet\"]')
        tweet_text = tweet_element.text
        return tweet_text
    except Exception as e:
        print(f"Failed to extract tweet text: {str(e)}")

    # Close the WebDriver
    driver.quit()


def get_reply(tweet_id):
    tweet_url = 'https://twitter.com/anyuser/status/' + tweet_id
    driver.get(tweet_url)

    # Wait for the page to load (you can adjust the waiting time as needed)
    driver.implicitly_wait(30)
    from selenium.webdriver.support.ui import WebDriverWait

    try:
        tweet_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#id__ex1uq296e91'))
        )
        tweet_text = tweet_element.text
        return tweet_text
    except Exception as e:
        print(
            f"Couldn't fetch data for tweet ID 1536848327979016193. Error: {e}")

    # Close the WebDriver
    driver.quit()


def parse_tweet(tweet_string):

    # Initialize an empty dictionary to store tweet data
    tweet_data = {}

    # Use regular expressions to extract information from the string
    username_match = re.search(r'@(\w+)', tweet_string)
    if username_match:
        tweet_data['username'] = username_match.group(1)

    tweet_match = re.search(
        r'(.+?)\n(\d+:\d+\s[APM]+)\s·\s([A-Za-z]+\s\d+,\s\d{4})', tweet_string)
    if tweet_match:
        tweet_data['text'] = tweet_match.group(1).strip()
        tweet_data['timestamp'] = tweet_match.group(2)
        tweet_data['date'] = tweet_match.group(3)

    views_match = re.search(r'(\d+\.\d+M)\sViews', tweet_string)
    if views_match:
        tweet_data['views'] = views_match.group(1)

    reposts_match = re.search(r'(\d+\.\d+K)\sReposts', tweet_string)
    if reposts_match:
        tweet_data['reposts'] = reposts_match.group(1)

    quotes_match = re.search(r'(\d+)\sQuotes', tweet_string)
    if quotes_match:
        tweet_data['quotes'] = quotes_match.group(1)

    likes_match = re.search(r'(\d+\.\d+K)\sLikes', tweet_string)
    if likes_match:
        tweet_data['likes'] = likes_match.group(1)

    bookmarks_match = re.search(r'(\d+)\sBookmarks', tweet_string)
    if bookmarks_match:
        tweet_data['bookmarks'] = bookmarks_match.group(1)

    return tweet_data


# Function to simulate get_tweet() (replace this with your actual implementation)

def get_tweet(tweet_id):
    return f"Tweet text for ID {tweet_id}"


# Define input and output file paths
input_file_path = '/Users/andrew/Desktop/community_notes_2/dataset/community_notes_trim.csv'
output_file_path = '/Users/andrew/Desktop/community_notes_2/dataset/community_notes_trim_updated.csv'

# Open the input CSV file for reading
with open(input_file_path, mode='r') as input_file:
    csv_reader = csv.DictReader(input_file)
    fieldnames = csv_reader.fieldnames

    # Create a temporary list to store rows with updated data
    updated_rows = []

    # Process the first 101 rows (0-100)
    for i, row in enumerate(csv_reader):
        if i <= 100:
            tweet_id = row['tweetId']
            try:
                tweet_text = get_tweet(tweet_id)
                # Update the 'tweetText' field with the tweet text
                row['text'] = parse_tweet().get('text')
                updated_rows.append(row)
                print(f"Worked on tweetID: {tweet_id}")
            except Exception as e:
                print(f"Error processing tweetID {tweet_id}: {str(e)}")
        else:
            break  # Stop processing after row 100

# Open the output CSV file for writing
with open(output_file_path, mode='w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write the updated rows
    writer.writerows(updated_rows)

print("CSV file updated successfully and saved to:", output_file_path)
