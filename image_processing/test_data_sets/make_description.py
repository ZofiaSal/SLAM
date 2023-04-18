import argparse
import os

# Create the parser
parser = argparse.ArgumentParser(description='Making description of pairs for SuperGlue')

# Add the arguments
parser.add_argument('--data', type=str, help='Data set directory name')

# Parse the arguments
args = parser.parse_args()

# Access the arguments
print(args.data)

catalogue = './test_data_sets/' + args.data + '/source_photos'
output_file = './test_data_sets/' + args.data + '/pairs_data/description.txt'

# Get a list of files in the catalogue directory, sorted alphabetically
files = sorted([f for f in os.listdir(catalogue) if f.endswith('.jpg')])

# Open the output file for writing
with open(output_file, 'w') as f:
    # Iterate over the list of files, skipping the last one
    for i in range(len(files)-1):
        # Write the pair of files to the output file
        f.write(files[i] + ' ' + files[i+1] + '\n')