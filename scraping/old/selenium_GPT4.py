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


def get_reply(tweet_id):
    tweet_url = 'https://twitter.com/anyuser/status/' + tweet_id
    driver.get(tweet_url)

    # Wait for the page to load (you can adjust the waiting time as needed)
    driver.implicitly_wait(30)
    try:
        tweet_element = driver.find_element(
            By.XPATH,
            '//div[@id=id__ex1uq296e91]')
        tweet_text = tweet_element.text
        return tweet_text
    except Exception as e:
        print(f"Failed to extract tweet text: {str(e)}")

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


# Assumed you have get_tweet and parse_tweet methods already defined


def main(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        # Create a CSV reader and writer object
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        # Write the header to the output CSV file
        csv_writer.writerow(['text', 'username', 'date', 'timestamp',
                            'views', 'reposts', 'quotes', 'likes', 'bookmarks'])

        # Skip the header in the input CSV if it exists
        next(csv_reader, None)

        # Counter for the number of processed tweets
        tweet_count = 0

        for row in csv_reader:
            if tweet_count >= 100:  # Stop after processing 100 tweets
                break

            # Assuming tweet_id is the first column in your input CSV
            tweet_id = row[0]
            tweet_string = get_tweet(tweet_id)
            tweet_data = parse_tweet(tweet_string)

            # Ensure that all the keys exist in tweet_data dictionary
            for key in ['text', 'username', 'date', 'timestamp', 'views', 'reposts', 'quotes', 'likes', 'bookmarks']:
                tweet_data.setdefault(key, 'N/A')

            # Write the row to the CSV
            csv_writer.writerow([tweet_data['text'], tweet_data['username'], tweet_data['date'], tweet_data['timestamp'],
                                 tweet_data['views'], tweet_data['reposts'], tweet_data['quotes'], tweet_data['likes'],
                                 tweet_data['bookmarks']])

            # Increment the counter
            tweet_count += 1


if __name__ == "__main__":
    # Define the input and output file paths
    input_file_path = '/Users/andrew/Desktop/community_notes_2/dataset/community_notes_trim.csv'
    output_file_path = '/Users/andrew/Desktop/community_notes_2/dataset/community_notes_trim_updated.csv'

    # Initialize the WebDriver outside the main function so it won't be created and destroyed in each iteration
    driver = webdriver.Chrome(
        executable_path='/Users/andrew/Desktop/community_notes_2/chromed/chromedriver')

    main(input_file_path, output_file_path)

    # Close the WebDriver
    driver.quit()
