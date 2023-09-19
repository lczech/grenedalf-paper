#!/usr/bin/python

# Aarahhahahaa, by using the split tool to create sync files,
# I accidentally destroyed the same names... the matrix only
# contains the xaa split file names now... but, I'm in a hurry,
# and so instead of running it nicely again, I'll try to bodge it.
# And you know what? That sounds like the perfect task for ChatGPT.
# Simple enough to be described in a few sentences, without having
# to think myself too much about file processing in python...

import csv

input = "fst-matrix.csv"
output = "fst-matrix-concise.csv"

# Define the paths to the replacement list files
replacement_files = ["xaa", "xab", "xac"]

# Initialize an empty dictionary for the replacements
replacements = {}

# Read each replacement list from its corresponding file
for file_name in replacement_files:
    with open(file_name, "r") as f:
        file_contents = [line.strip() for line in f]
        replacements[file_name] = [path.split("/")[-1].replace(".csv", "") for path in file_contents]

# Open the input and output CSV files
with open(input, "r") as input_file, open(output, "w") as output_file:
    # Create the CSV reader and writer objects
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # Iterate over each row in the input CSV file
    for row in reader:
        # Iterate over each cell in the row
        for i, cell in enumerate(row):

            # Check if the cell content matches the pattern
            if cell.startswith("counts-") and ":" in cell:
                prefix, index = cell.split(":")
                prefix = prefix[len("counts-"):]
                if prefix in replacements:
                    # Lookup the replacement value from the dictionary
                    replacements_list = replacements[prefix]
                    replacement_index = int(index) - 1
                    if replacement_index < len(replacements_list):
                        # Replace the cell content with the replacement value
                        row[i] = replacements_list[replacement_index]

        # Write the modified row to the output CSV file
        writer.writerow(row)
