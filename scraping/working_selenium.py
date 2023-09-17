from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Make sure that this import statement is correct
if hasattr(webdriver, 'find_element_by_xpath'):
    print("find_element_by_xpath is available")
else:
    print("find_element_by_xpath is not available")

# Initialize the Chrome Driver
driver_path = '/Users/andrew/Desktop/community_notes_2/chromed/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)

# Load the dataset
dataset_path = '/Users/andrew/Desktop/community_notes_2/dataset/community_notes_trim.csv'
df = pd.read_csv(dataset_path)

# Initialize an empty DataFrame to store the results
result_df = pd.DataFrame(columns=['tweetId', 'tweetText'])

# Loop through the first 100 tweet IDs
for tweet_id in df['tweetId'][101:1400]:
    tweet_url = f"https://twitter.com/anyuser/status/{str(tweet_id)}"
    driver.get(tweet_url)

    time.sleep(30)

    try:
        tweet_element = driver.find_element(
            By.CSS_SELECTOR,
            '[data-testid=\"tweet\"]')
        tweet_text = tweet_element.text
        result_df = result_df.append(
            {'tweetId': tweet_id, 'tweetText': tweet_text}, ignore_index=True)
    except Exception as e:
        print(f"Couldn't fetch data for tweet ID {tweet_id}. Error: {e}")


# Save the new dataset
result_df.to_csv(
    '/Users/andrew/Desktop/community_notes_2/dataset/community_notes_with_text.csv', index=False)

# Close the Selenium driver
driver.quit()
