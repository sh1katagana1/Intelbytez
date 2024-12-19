# Compare-Unique Script

***

## Goal
To create a script that takes in a text file of subdomains on each line called a.txt and takes in a second text file of subdomains on each line called b.txt. Compare the two files and if b.txt has any subdomains on a line that a.txt does not have, print these domains to a third file called c.txt

## Script
```
def compare_subdomains(file_a, file_b, output_file):
    with open(file_a, 'r') as a, open(file_b, 'r') as b:
        subdomains_a = set(a.read().splitlines())
        subdomains_b = set(b.read().splitlines())
    
    unique_subdomains = subdomains_b - subdomains_a
    
    with open(output_file, 'w') as c:
        for subdomain in unique_subdomains:
            c.write(f"{subdomain}\n")

# Usage
compare_subdomains('a.txt', 'b.txt', 'c.txt')
```
## What does this script do?
This script does the following:

1. It defines a function compare_subdomains that takes three file names as input: file_a, file_b, and output_file.
2. It opens both input files and reads their contents, splitting them into sets of subdomains
3. It finds the unique subdomains in b.txt by subtracting the set of subdomains from a.txt.
4. It writes the unique subdomains to the output file c.txt, one per line

## Usage
To use this script, save it as a Python file (e.g., compare_subdomains.py) and run it. Make sure a.txt and b.txt are in the same directory as the script. The script will create c.txt with the unique subdomains from b.txt.