import csv

# Open the input file for reading
with open('processed_tweets_4.csv', 'r') as infile:
    csvreader = csv.reader(infile)

    # Open the output file for writing
    with open('enumerated_processed_tweets_4.csv', 'w', newline='') as outfile:
        csvwriter = csv.writer(outfile)

        # Enumerate through rows
        for i, row in enumerate(csvreader):
            # Prepend the row number to the row data
            new_row = [i-1] + row
            csvwriter.writerow(new_row)
