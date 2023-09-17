import pandas as pd
import re

# Read the dataset
df = pd.read_csv(
    '/Users/andrew/Desktop/community_notes_2/dataset/scraped_tweets.csv')

# Initialize lists to store the new columns
n = len(df)
names = [None] * n
usernames = [None] * n
tweet_texts = [None] * n
note_texts = [None] * n
timestamps = [None] * n
metrics = [None] * n
# Loop through the tweetText column
with open('output.txt', 'w') as f:
    for i, tweet in enumerate(df['tweetText']):
        print(f"\n ---- Processing row {i} ----", file=f)  # Debug
        lines = tweet.split('\n')

        # Initialize local variables
        tweet_text = []
        note_text = []
        mode = 'tweet_text'

        for idx, line in enumerate(lines):
            if idx == 0:
                names[i] = line
                continue
            elif idx == 1:
                usernames[i] = line
                continue

            # Switch modes based on special lines
            if "Readers added context they thought people might want to know" in line:
                mode = 'note_text'
                continue
            elif re.match(r'\d{1,2}:\d{2} [APMapm]{2} · \w{3} \d{1,2}, \d{4}', line):
                timestamps[i] = line
                mode = 'metrics'
                continue

            # Add lines based on current mode
            if mode == 'tweet_text':
                tweet_text.append(line)
            elif mode == 'note_text':
                note_text.append(line)
            elif mode == 'metrics':
                metrics[i] = line
                print(line, file=f)

        # Save text data
        tweet_texts[i] = ' '.join(tweet_text) if tweet_text else None
        note_texts[i] = ' '.join(note_text) if note_text else None


# Update DataFrame columns
df['name'] = names
df['username'] = usernames
df['tweet_text'] = tweet_texts
df['note_text'] = note_texts
df['timestamp'] = timestamps
df['metrics'] = metrics

# Save the DataFrame with the new columns
df.to_csv('processed_tweets_4.csv', index=False)
