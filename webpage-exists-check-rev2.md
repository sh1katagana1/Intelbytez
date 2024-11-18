# Webpage Exists Checker Rev2

***

## Goal
To create a script that takes in a list of domains from a text file and attempts to connect to each one using a User Agent string for a Chrome browser. If the connection has redirects, follow all redirects and print the redirect URLs to the screen. If the connection is successful, print the final URL to the screen. If the final URL has a 403 HTTP response code, print "has 403" and the final URL after its last redirect happens. If it cannot connect after 10 seconds, stop trying to connect, omit it from the results and move to the next domain.

## Script (Python)
```
import requests
from urllib.parse import urlparse
import sys

def check_domain(domain, user_agent):
    url = f"https://{domain}"
    headers = {'User-Agent': user_agent}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        # Print redirect chain
        if len(response.history) > 0:
            print(f"Redirects for {domain}:")
            for r in response.history:
                print(f"  {r.url}")
        
        # Print final URL
        final_url = response.url
        print(f"Final URL for {domain}: {final_url}")
        
        # Check for 403 status code
        if response.status_code == 403:
            print(f"  has 403: {final_url}")
        
    except requests.exceptions.RequestException:
        print(f"Could not connect to {domain}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    try:
        with open(input_file, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
        
        for domain in domains:
            check_domain(domain, user_agent)
            print()  # Add a blank line between domain results
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```
## What does this script do?

1. It imports the necessary libraries: requests for making HTTP requests, urlparse from urllib.parse for URL parsing, and sys for command-line arguments.
2. The check_domain function takes a domain and a user agent string as input. It attempts to connect to the domain using HTTPS and follows all redirects.
3. If there are redirects, it prints the redirect chain.
4. It prints the final URL after all redirects.
5. If the final response has a 403 status code, it prints "has 403" along with the final URL.
6. If it can't connect within 10 seconds, it prints an error message and moves to the next domain.
7. The main function reads domains from a text file specified as a command-line argument.
8. It uses a Chrome user agent string for the requests.
9. It processes each domain in the file, calling check_domain for each one.

## Usage

1. Save it as a Python file (e.g., check_domains.py).
2. Create a text file with one domain per line (e.g., domains.txt).
3. Run the script from the command line:

```
python check_domains.py domains.txt
```
This script will process each domain in the file, following redirects, and provide the requested output for each domain