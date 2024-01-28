import csv
import ast

# Define input and output file paths
input_file = "random_live_data.txt"
output_file = "random_live_data.csv"

# Read the data from the text file
with open(input_file, 'r') as file:
    data = file.read()

# Convert the string representation of list of dictionaries into Python objects
data_list = ast.literal_eval(data)

# Extract field names from the first dictionary in the list
fieldnames = data_list[0].keys()

# Write data to CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write rows
    for item in data_list:
        writer.writerow(item)

print("CSV file has been created successfully.")
