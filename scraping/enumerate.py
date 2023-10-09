import csv

# Open the input file for reading
with open('final_raw.csv', 'r') as infile:
    csvreader = csv.reader(infile)

    # Open the output file for writing
    with open('dfinal_raw.csv', 'w', newline='') as outfile:
        csvwriter = csv.writer(outfile)

        # Enumerate through rows
        for i, row in enumerate(csvreader):
            # Prepend the row number to the row data
            new_row = [i-1] + row
            csvwriter.writerow(new_row)
