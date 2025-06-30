# Shodan Favicon Check

***

## Goal
Create a script that takes in a text file list of favicon hashes, called hashes.txt, searches Shodan for any website using that has and return the results in Excel format. You will need to put in your Shodan API key for this.

## Language
Python

## Script
```
import shodan
import time
import csv

# Replace with your actual Shodan API key
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'

# Initialize the Shodan API
api = shodan.Shodan(SHODAN_API_KEY)

def search_by_favicon_hash(hash_value):
    results_list = []
    try:
        query = f'http.favicon.hash:{hash_value}'
        results = api.search(query)
        print(f"\n[+] Found {results['total']} results for hash {hash_value}")
        for result in results['matches']:
            ip = result.get('ip_str', '')
            port = result.get('port', '')
            hostnames = ','.join(result.get('hostnames', []))
            results_list.append({
                'hash': hash_value,
                'ip': ip,
                'port': port,
                'hostnames': hostnames
            })
    except shodan.APIError as e:
        print(f"[-] Error searching for hash {hash_value}: {e}")
        time.sleep(1)
    return results_list

def main():
    input_file = 'hashes.txt'
    output_file = 'favicon_results.csv'
    all_results = []

    try:
        with open(input_file, 'r') as file:
            hashes = [line.strip() for line in file if line.strip()]
        
        for hash_value in hashes:
            results = search_by_favicon_hash(hash_value)
            all_results.extend(results)
            time.sleep(1)

        # Write results to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['hash', 'ip', 'port', 'hostnames']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_results:
                writer.writerow(row)

        print(f"\n[+] Results saved to {output_file}")

    except FileNotFoundError:
        print(f"[-] File '{input_file}' not found.")
    except Exception as e:
        print(f"[-] Unexpected error: {e}")

if __name__ == '__main__':
    main()
```
