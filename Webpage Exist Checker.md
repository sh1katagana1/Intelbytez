# Webpage Exist Checker

***


## Goal
To create a script that takes in a list of domains from a text file, tries to connect to it, following all redirects and printing all redirects to screen. If the final page is HTTP response code 200, print the first 100 words of the HTTP response. If it cannot connect, then output a string that says "there is no webpage here"

## Script
```
import requests
from bs4 import BeautifulSoup
import sys

def process_domain(domain):
    try:
        # Send a GET request to the domain, following redirects
        response = requests.get(f"http://{domain}", allow_redirects=True)
        
        # Print all redirects
        for i, resp in enumerate(response.history):
            print(f"Redirect {i+1}: {resp.url}")
        
        # Print final URL
        print(f"Final URL: {response.url}")
        
        # Check if the final response is 200 OK
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text and split into words
            words = soup.get_text().split()
            
            # Print the first 100 words
            print("First 100 words of the response:")
            print(" ".join(words[:100]))
        else:
            print(f"Final status code: {response.status_code}")
    
    except requests.RequestException:
        print("There is no webpage here")
    
    print("\n" + "-"*50 + "\n")

def main(filename):
    with open(filename, 'r') as file:
        domains = file.read().splitlines()
    
    for domain in domains:
        print(f"Processing domain: {domain}")
        process_domain(domain)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    main(sys.argv[1])
```

## What does the script do?

1. It imports the necessary libraries: requests for making HTTP requests, BeautifulSoup for parsing HTML, and sys for handling command-line arguments.
2. The process_domain function takes a domain as input and:
3. Sends a GET request to the domain, following all redirects.
4. Prints all redirects encountered.
5. If the final response has a status code of 200, it extracts and prints the first 100 words of the response.
6. If there's an error connecting to the website, it prints "There is no webpage here".
7. The main function reads domains from a text file and processes each domain.
8. The script checks for the correct usage (providing a filename as an argument) and runs the main function.

## Usage

1. Save it as a Python file (e.g., domain_checker.py).
2. Create a text file with a list of domains, one per line.
3. Run the script from the command line, providing the filename as an argument:

```
python domain_checker.py domains.txt
```

This script will process each domain in the file, following redirects, printing redirect information, and either displaying the first 100 words of the response or indicating that there's no webpage available