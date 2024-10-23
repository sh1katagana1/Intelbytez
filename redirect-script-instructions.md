# Redirect Script Instructions

## Goal
Create a script that takes in a list of domain names, attempts to connect to them, following redirects, and prints to console all of the redirects that happen for each domain.

## Script
```
import requests
import sys

def follow_redirects(domain):
    try:
        url = f"http://{domain}"
        response = requests.get(url, allow_redirects=True, timeout=10)
        
        print(f"\nRedirects for {domain}:")
        if len(response.history) > 0:
            for i, r in enumerate(response.history, 1):
                print(f"  {i}. {r.url} -> {r.headers['Location']}")
            print(f"  Final: {response.url}")
        else:
            print("  No redirects")
    except requests.exceptions.RequestException as e:
        print(f"  Error: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <domain_list_file>")
        sys.exit(1)

    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    except IOError:
        print(f"Error: Unable to read file '{filename}'")
        sys.exit(1)

    for domain in domains:
        follow_redirects(domain)

if __name__ == "__main__":
    main()
```

## What does the script do?

1. It imports the necessary libraries: requests for making HTTP requests and sys for command-line arguments.
2. The follow_redirects function takes a domain name as input, attempts to connect to it, and prints all redirects that occur.
3. The main function reads the domain names from a text file specified as a command-line argument.
4. For each domain in the file, it calls the follow_redirects function
5. The script handles potential errors, such as connection issues or invalid domains

## Usage:

1. Save it to a file, e.g., domain_redirects.py.
2. Create a text file with a list of domains, one per line.
3. Run the script from the command line, passing the domain list file as an argument:

```
python domain_redirects.py domain_list.txt
```

The script will attempt to connect to each domain, follow any redirects, and print the redirect chain to the console. It will handle both HTTP and HTTPS redirects automatically. Note that this script uses the requests library, which you may need to install if it's not already available:

```
pip install requests
```

***


## Modification
We can also modify it to output the results to an Excel file. 

## Script
```
import requests
import openpyxl
from urllib.parse import urlparse

def follow_redirects(url):
    redirects = []
    try:
        response = requests.get(url, allow_redirects=True, timeout=10)
        for resp in response.history:
            redirects.append(resp.url)
        redirects.append(response.url)
    except requests.exceptions.RequestException:
        pass
    return redirects

def process_domains(input_file, output_file):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Domain", "Redirects"])

    with open(input_file, 'r') as f:
        domains = f.read().splitlines()

    for domain in domains:
        if not domain.startswith('http'):
            domain = f'http://{domain}'
        
        redirects = follow_redirects(domain)
        
        if redirects:
            ws.append([domain, ' -> '.join(redirects)])
        else:
            ws.append([domain, "No redirects or error"])

    wb.save(output_file)

# Usage
input_file = 'domains.txt'
output_file = 'redirects.xlsx'
process_domains(input_file, output_file)
```

## What does this script do?

1. We define a follow_redirects function that takes a URL, sends a GET request, and returns a list of all redirects encountered.
2. The process_domains function reads domains from a text file, processes each domain, and writes the results to an Excel file.
3. For each domain, we ensure it starts with 'http://' if not already specified.
4. We follow the redirects for each domain and write the results to the Excel file.
5. If there are no redirects or an error occurs, we note that in the Excel file.

## Usage

1. Install the required libraries:

```
pip install requests openpyxl
```

2. Create a text file named domains.txt with one domain per line.
3. Run the script. It will create an Excel file named redirects.xlsx with the results.





