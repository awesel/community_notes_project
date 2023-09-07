from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Create a WebDriver instance (you need to specify the path to your driver executable)
driver = webdriver.Chrome(executable_path='./chromed/chromedriver')

# Replace 'tweet_url' with the actual tweet URL
tweet_url = 'https://twitter.com/sajzxa/status/1699570836532015404'
driver.get(tweet_url)

# Wait for the page to load (you can adjust the waiting time as needed)
driver.implicitly_wait(20)
try:
    tweet_element = driver.find_element(
        By.CSS_SELECTOR, '[data-testid=\"tweet\"]')
    tweet_text = tweet_element.text
    print(tweet_text)
except Exception as e:
    print(f"Failed to extract tweet text: {str(e)}")

# Close the WebDriver
driver.quit()
