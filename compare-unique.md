
## Goal
To create a script that takes in a text file of subdomains on each line called a.txt and a second text file called b.txt that has a list of subdomains on each line. Compare the two text files and find lines that are not in both files and print them to a third text file called c.txt

## Script
```
def compare_files(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        set1 = set(f1.read().splitlines())
        set2 = set(f2.read().splitlines())

    unique_lines = set1.symmetric_difference(set2)

    with open(output_file, 'w') as f_out:
        for line in unique_lines:
            f_out.write(line + '\n')

compare_files('a.txt', 'b.txt', 'c.txt')
```

## What does this script do?
This script does the following:

1. It defines a function compare_files that takes three parameters: file1, file2, and output_file
2. It opens both input files and reads their contents into sets, removing any newline characters
3. It uses the symmetric_difference method to find lines that are in either set but not in both
4. It writes the unique lines to the output file, adding a newline character after each line
5. Finally, it calls the function with the specified file names: 'a.txt', 'b.txt', and 'c.txt'

## Usage

To use this script, save it as a .py file and run it in the same directory as your input files. It will create a new file 'c.txt' containing the unique subdomains.