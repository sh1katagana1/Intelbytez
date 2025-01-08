# MXToolBox DNS Info Script

***


## Goal
To create a script that takes in a domain name as input and checks it against the MXToolbox SuperTool DNS lookup and returns the results to screen

## Script
```
import requests
import json

def mxtoolbox_dns_lookup(domain):
    url = f"https://api.mxtoolbox.com/api/v1/lookup/dns/{domain}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(f"DNS Lookup Results for {domain}:")
        print("-----------------------------------")
        
        for record in data.get("Information", []):
            print(f"Type: {record.get('Type')}")
            print(f"Domain Name: {record.get('Domain Name')}")
            print(f"IP Address: {record.get('IP Address')}")
            print(f"TTL: {record.get('TTL')}")
            print("-----------------------------------")
        
        if not data.get("Information"):
            print("No DNS records found.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    domain = input("Enter a domain name: ")
    mxtoolbox_dns_lookup(domain)
```

## What does this script do?
This script does the following:

1. It imports the necessary libraries: requests for making HTTP requests and json for parsing JSON data    
2. The mxtoolbox_dns_lookup function takes a domain name as input and constructs the URL for the MXToolbox API
3. It sends a GET request to the MXToolbox API and handles any potential errors1
4. If successful, it parses the JSON response and prints the DNS lookup results, including the record type, name, data, and TTL for each record found
5. If no records are found, it prints a message indicating so.
6. The script prompts the user to enter a domain name and then calls the lookup function with that input.

## Usage
To use this script:

1. Save it to a file (e.g., mxtoolbox_lookup.py).
2. Install the requests library if you haven't already (pip install requests).
3. Run the script (python mxtoolbox_lookup.py).
4. Enter a domain name when prompted.



## Modification
Modify the above code to utilize an MX Toolbox API key(as you will likely get an error about that from the previous script):

## Script
```
import requests
import json

def mxtoolbox_dns_lookup(domain, api_key):
    url = f"https://api.mxtoolbox.com/api/v1/lookup/dns/{domain}"
    headers = {"Authorization": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"DNS Lookup Results for {domain}:")
        print("-----------------------------------")
        
        for record in data.get("Information", []):
            print(f"Type: {record.get('Type')}")
            print(f"Domain Name: {record.get('Domain Name')}")
            print(f"IP Address: {record.get('IP Address')}")
            print(f"TTL: {record.get('TTL')}")
            print("-----------------------------------")
        
        if not data.get("Information"):
            print("No DNS records found.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    domain = input("Enter a domain name: ")
    api_key = input("Enter your MXToolbox API key: ")
    mxtoolbox_dns_lookup(domain, api_key)
```

## What does this script do?
This updated script makes the following changes:

1. The mxtoolbox_dns_lookup function now takes an additional parameter api_key.
2. We create a headers dictionary that includes the API key in the "Authorization" header.
3. The requests.get() call now includes the headers parameter.
4. In the main block, we prompt the user to enter their MXToolbox API key.

## Usage
To use this script:

1. Save it to a file (e.g., mxtoolbox_lookup.py).
2. Install the requests library if you haven't already (pip install requests).
3. Run the script (python mxtoolbox_lookup.py).
4. Enter a domain name when prompted.
5. Enter your MXToolbox API key when prompted.

Note that you'll need to obtain an API key from MXToolbox to use their API. You can hardcode the API key for testing locally, saves having to paste that in every run.


## Modification 2
Modify this script to take in a text file list of domain names as the input

## Script
```
import requests

def mxtoolbox_dns_lookup(domain, api_key):
    url = f"https://api.mxtoolbox.com/api/v1/lookup/dns/{domain}"
    headers = {"Authorization": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"\nDNS Lookup Results for {domain}:")
        print("-----------------------------------")
        
        for record in data.get("Information", []):
            print(f"Type: {record.get('Type')}")
            print(f"Domain Name: {record.get('Domain Name')}")
            print(f"IP Address: {record.get('IP Address')}")
            print(f"TTL: {record.get('TTL')}")
            print("-----------------------------------")
        
        if not data.get("Information"):
            print("No DNS records found.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred for {domain}: {e}")

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    input_file = input("Enter the path to the text file containing domain names: ")
    api_key = input("Enter your MXToolbox API key: ")
    
    domains = read_domains_from_file(input_file)
    
    for domain in domains:
        mxtoolbox_dns_lookup(domain, api_key)
```

## What does this modification do?
This modified script does the following:

1. We've added a new function read_domains_from_file that reads domain names from a text file and returns them as a list
2. In the main block, we prompt the user to enter the path to the text file containing domain names instead of a single domain name
3. We use the read_domains_from_file function to get a list of domains from the input file
4. We then iterate through each domain in the list and perform the DNS lookup for each one

## Usage
To use this script:

1. Create a text file with one domain name per line.
2. Run the script and enter the path to your text file when prompted.
3. Enter your MXToolbox API key when prompted.

The script will then perform DNS lookups for all domains in the file and display the results for each


## Modification 3
I made some changes by adding some other sections of the API as well as its fields that I want to pull. Now I want to be able to export the results to Excel file format where the column names reflect the Keys in the key:value pairs from the script:

## Script
```
import requests
import json
import pandas as pd

def mxtoolbox_dns_lookup(domain, api_key):
    url = f"https://api.mxtoolbox.com/api/v1/lookup/dns/{domain}"
    headers = {"Authorization": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(f"DNS Lookup Results for {domain}:")
        print("-----------------------------------")
        
        information_data = []
        transcript_data = []
        
        for record in data.get("Information", []):
            print(f"Type: {record.get('Type')}")
            print(f"Domain Name: {record.get('Domain Name')}")
            print(f"IP Address: {record.get('IP Address')}")
            print(f"Asn: {record.get('Asn')}")
            print(f"Status: {record.get('Status')}")
            print("-----------------------------------")
            information_data.append(record)
        
        for record in data.get("Transcript", []):
            print(f"ServerName: {record.get('ServerName')}")
            print(f"ServerIP: {record.get('ServerIP')}")
            transcript_data.append(record)
        
        if not data.get("Information"):
            print("No DNS records found.")
        if not data.get("Transcript"):
            print("No DNS Information")
        
        # Export to Excel
        with pd.ExcelWriter(f"{domain}_dns_lookup.xlsx") as writer:
            if information_data:
                pd.DataFrame(information_data).to_excel(writer, sheet_name="Information", index=False)
            if transcript_data:
                pd.DataFrame(transcript_data).to_excel(writer, sheet_name="Transcript", index=False)
        
        print(f"Results exported to {domain}_dns_lookup.xlsx")
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    domain = input("Enter a domain name: ")
    api_key = input("Enter your MxToolbox API key: ")
    mxtoolbox_dns_lookup(domain, api_key)
```

## What does this modification do?
This modified script adds the functionality to export the results to an Excel file. Here are the key changes:

1. We import the pandas library to handle the Excel export.
2. We create two lists, information_data and transcript_data, to store the records from the "Information" and "Transcript" sections respectively.
3. After printing the results, we use pandas to create an Excel file:
4. We use pd.ExcelWriter to create an Excel file named {domain}_dns_lookup.xlsx.
5. We create two separate sheets: "Information" and "Transcript".
6. We convert the data lists to DataFrames and write them to their respective sheets.
7. We set index=False to prevent pandas from adding an extra index column.
8. Finally, we print a message confirming that the results have been exported to the Excel file.

This script will create an Excel file with two sheets, "Information" and "Transcript", containing the DNS lookup results. The column names in the Excel file will match the key names from the API response.


## Final Modification
Now that all of that works well, I want to be able to pass in a text file list of domains instead of typing one at the prompt:

## Script
```
import requests
import json
import pandas as pd

def mxtoolbox_dns_lookup(domains, api_key):
    results = []
    
    for domain in domains:
        url = f"https://api.mxtoolbox.com/api/v1/lookup/dns/{domain.strip()}"
        headers = {"Authorization": api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            print(f"DNS Lookup Results for {domain.strip()}:")
            print("-----------------------------------")
            
            information_data = data.get("Information", [])
            transcript_data = data.get("Transcript", [])
            
            for record in information_data:
                print(f"Type: {record.get('Type')}")
                print(f"Domain Name: {record.get('Domain Name')}")
                print(f"IP Address: {record.get('IP Address')}")
                print(f"Asn: {record.get('Asn')}")
                print(f"Status: {record.get('Status')}")
                print("-----------------------------------")
            
            for record in transcript_data:
                print(f"ServerName: {record.get('ServerName')}")
                print(f"ServerIP: {record.get('ServerIP')}")
            
            if not information_data:
                print("No DNS records found.")
            if not transcript_data:
                print("No DNS Information")
            
            results.append({
                "domain": domain.strip(),
                "information": information_data,
                "transcript": transcript_data
            })
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred for {domain.strip()}: {e}")
    
    return results

if __name__ == "__main__":
    api_key = input("Enter your MxToolbox API key: ")
    
    with open("domains.txt", "r") as file:
        domains = file.readlines()
    
    results = mxtoolbox_dns_lookup(domains, api_key)
    
    # Export to Excel
    with pd.ExcelWriter("dns_lookup_results.xlsx") as writer:
        for result in results:
            domain = result["domain"]
            if result["information"]:
                pd.DataFrame(result["information"]).to_excel(writer, sheet_name=f"{domain}_Information", index=False)
            if result["transcript"]:
                pd.DataFrame(result["transcript"]).to_excel(writer, sheet_name=f"{domain}_Transcript", index=False)
    
    print("Results exported to dns_lookup_results.xlsx")
```

## What does this modification do?
This modified script allows you to input multiple domains from a text file called "domains.txt". Here are the key changes:

1. The script now reads domains from a file named "domains.txt" instead of prompting for a single domain input5
2. The mxtoolbox_dns_lookup function now accepts a list of domains and processes them in a loop3
3. Results for all domains are stored in a list of dictionaries, where each dictionary contains the domain name and its corresponding information and transcript data.
4. The Excel export now creates separate sheets for each domain's Information and Transcript data, naming them accordingly4
5. The output Excel file is now named "dns_lookup_results.xlsx" to reflect that it contains results for multiple domains.

## Usage
To use this script:

1. Create a text file named "domains.txt" in the same directory as the script.
2. Add one domain name per line in the "domains.txt" file.
3. Run the script and enter your MxToolbox API key when prompted.

The script will process all domains in the file and export the results to a single Excel file with multiple sheets



