import pandas as pd
import re

# Read CSV file
df = pd.read_csv('scraped_data.csv')


# Remove all commas from the "metrics" column
df['metrics'] = df['metrics'].str.replace(',', '')


# Initialize new columns with default value "None"
df['Views'] = 'None'
df['Reposts'] = 'None'
df['Quotes'] = 'None'
df['Likes'] = 'None'
df['Bookmarks'] = 'None'

# Define a function to update metric columns


def update_metrics(row):
    metrics_str = row['metrics']
    if pd.isnull(metrics_str):
        return row

    # Define the metrics to look for
    metrics_to_extract = ['Views', 'Reposts', 'Quotes', 'Likes', 'Bookmarks']

    # Use regular expressions to extract metrics
    for metric in metrics_to_extract:
        match = re.search(f'([0-9.]+[KkMm]?)(?=\\s*{metric})', metrics_str)
        if match:
            # Convert K and M to actual numbers
            value_str = match.group(1)
            if 'K' in value_str:
                value = float(value_str.replace('K', '')) * 1e3
            elif 'M' in value_str:
                value = float(value_str.replace('M', '')) * 1e6
            else:
                value = float(value_str)

            row[metric] = value
    return row


# Apply the function to update metric columns
df = df.apply(update_metrics, axis=1)

# Save the DataFrame with new columns back to CSV
df.to_csv('updated_scraped_data.csv', index=False)
