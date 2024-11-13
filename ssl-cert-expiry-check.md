# SSL Certificate Expiry Checker

***

## Goal
To create a python3 script that takes in a list of domains from a text file and finds the SSL certificate expiration date and outputs the details to an excel file

## Script
```
import ssl
import socket
from datetime import datetime
import pandas as pd
import concurrent.futures

def get_ssl_expiry(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                cert = secure_sock.getpeercert()
                expiration_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiration_date - datetime.now()).days
                return domain, expiration_date.strftime('%Y-%m-%d'), days_until_expiry
    except Exception as e:
        return domain, "Error", str(e)

def process_domains(domains):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(get_ssl_expiry, domains))
    return results

def main():
    # Read domains from file
    with open('domains.txt', 'r') as file:
        domains = [line.strip() for line in file if line.strip()]

    # Process domains
    results = process_domains(domains)

    # Create DataFrame
    df = pd.DataFrame(results, columns=['Domain', 'Expiration Date', 'Days Until Expiry/Error'])

    # Write to Excel
    df.to_excel('ssl_expiry_results.xlsx', index=False)
    print("Results have been written to ssl_expiry_results.xlsx")

if __name__ == "__main__":
    main()
```

## What does the script do?

1. It defines a function get_ssl_expiry that takes a domain name, connects to it, retrieves the SSL certificate, and extracts the expiration date    .
2. The process_domains function uses a ThreadPoolExecutor to check multiple domains concurrently, improving performance

The main function:
1. Reads domains from a file named 'domains.txt'
2. Processes the domains to get their SSL certificate expiration information
3. Creates a pandas DataFrame with the results
4. Writes the results to an Excel file named 'ssl_expiry_results.xlsx'

## Usage

1. Save it as a .py file (e.g., ssl_checker.py).
2. Create a text file named domains.txt in the same directory, with one domain per line. 
3. Install the required libraries if you haven't already:
```
pip install pandas openpyxl
```
4. Run the script:
```
python ssl_checker.py
```
The script will process the domains and create an Excel file named ssl_expiry_results.xlsx with columns for Domain, Expiration Date, and Days Until Expiry (or Error message if there was a problem checking the certificate). 
