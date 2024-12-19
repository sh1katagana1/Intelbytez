
## Goal
To create a script that takes in a text file of subdomains. Each line is a subdomain separated by periods. Have the script sort alphabetically by the last to values separated by periods on each line.

## Script
```
def sort_key(subdomain):
    parts = subdomain.strip().split('.')
    return tuple(parts[-2:])

with open('subdomains.txt', 'r') as file:
    subdomains = file.readlines()

sorted_subdomains = sorted(subdomains, key=sort_key)

with open('sorted_subdomains.txt', 'w') as file:
    file.writelines(sorted_subdomains)

print("Subdomains sorted and saved to 'sorted_subdomains.txt'")
```

## What does this script do?
This script does the following:

1. We define a sort_key function that splits each subdomain by periods and returns a tuple of the last two parts
2. The script reads the subdomains from a file named 'subdomains.txt'
3. It then sorts the subdomains using the sorted() function with our custom sort_key
4. Finally, it writes the sorted subdomains to a new file named 'sorted_subdomains.txt'

## Usage
To use this script:

1. Save it as a .py file (e.g., sort_subdomains.py).
2. Create a text file named 'subdomains.txt' in the same directory, with each subdomain on a new line.
3. Run the script using python sort_subdomains.py.

The script will create a new file 'sorted_subdomains.txt' with the sorted subdomains.