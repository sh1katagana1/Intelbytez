# Updated CRT.SH Check Script 2025

***

## Goal
To create a script that takes in a text file list of domain names, then queries crt.sh for SSL certificate details. Have it output this in excel 

## Script (Python)
```
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_cert_details(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def process_domain(domain):
    cert_details = get_cert_details(domain)
    if cert_details:
        return [
            {
                'domain': domain,
                'common_name': cert['common_name'],
                'issuer_name': cert['issuer_name'],
                'not_before': cert['not_before'],
                'not_after': cert['not_after']
            }
            for cert in cert_details
        ]
    return []

def main():
    input_file = 'domains.txt'  # Replace with your input file name
    output_file = 'cert_details.xlsx'  # Replace with your desired output file name

    with open(input_file, 'r') as f:
        domains = [line.strip() for line in f]

    all_cert_details = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_domain = {executor.submit(process_domain, domain): domain for domain in domains}
        for future in as_completed(future_to_domain):
            all_cert_details.extend(future.result())

    df = pd.DataFrame(all_cert_details)
    df.to_excel(output_file, index=False)
    print(f"Certificate details saved to {output_file}")

if __name__ == "__main__":
    main()
```

## What does the script do?
This script does the following:
1. It reads domain names from a text file (default name: 'domains.txt')6.
2. For each domain, it queries crt.sh using the JSON API9.
3. It processes the certificate details for each domain concurrently using ThreadPoolExecutor for improved performance7.
4. The script extracts relevant information such as common name, issuer name, and validity dates for each certificate10.
5. Finally, it saves all the collected certificate details to an Excel file (default name: 'cert_details.xlsx') using pandas2.

## Usage
To use this script:
```
pip3 install requests pandas openpyxl
```
1. Install the required libraries: pip install requests pandas openpyxl
2. Create a text file named 'domains.txt' with one domain name per line.
3. Run the script. It will process the domains and create an Excel file with the certificate details.

You can customize the input and output file names by modifying the input_file and output_file variables in the main() function.
