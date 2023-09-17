import csv
# Initialize an empty dictionary to hold the results
output_dict = {}

# Variable to keep track of the current row number
current_row = None


def extract_integer_slice(s):
    start = s.index("row ") + len("row ")
    end = s.index(" ----", start)
    return int(s[start:end])


# Variable to hold the content for each row
current_content = ""

# Open the file and read it line-by-line
with open('output.txt', 'r') as file:
    for line in file:

        # Remove leading and trailing whitespace
        line = line.strip()
        # If the line starts with "---- Processing row", we are starting a new row
        if line.startswith("---- Processing row"):
            # Save the previous row's content to the dictionary
            if current_row is not None:
                output_dict[current_row] = current_content.strip()
                print(current_row)

            # Reset the current_content and set the new current_row
            # Extract the row number using slicing
            current_row = extract_integer_slice(line)
            current_content = ""
        else:
            # Append the line to current_content
            current_content += line + "\n"

# Don't forget to save the last row
if current_row is not None:
    output_dict[current_row] = current_content.strip()

# Print the dictionary to see the output
print(output_dict[0])

# Read the input CSV file and write to a new output CSV file
with open("processed_4.csv", "r", newline="") as infile, open("update_processed_4.csv", "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        numba = row.get("rowNumber", None)
        row["metrics"] = output_dict[int(numba)]
        writer.writerow(row)
