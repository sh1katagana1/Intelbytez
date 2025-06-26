# HIBP Script Instructions

***

## Goal
To create a script that takes a text file list of email addresses as input and checks them against the haveibeenpwned APIv3 to see if they were compromised. Allows me to hardcode my API key in the script. Based on this page https://haveibeenpwned.com/API/v3#AllDataClasses The fields I add in for output are Name, Title, BreachDate, Description, DataClasses. This data will be listed in json format after each email found to be compromised.

## Language
Python

## Script
```
import requests
import json
import time

# Hardcode your API key here
API_KEY = 'YOUR_HIBP_API_KEY'
USER_AGENT = 'YourAppName/1.0'  # Change this to the name of your app/script

# Path to the input file containing email addresses (one per line)
INPUT_FILE = 'emails.txt'

# HIBP API endpoint for breach search by account
API_URL = 'https://haveibeenpwned.com/api/v3/breachedaccount/{}'

# Read email addresses from file
with open(INPUT_FILE, 'r') as f:
    emails = [line.strip() for line in f if line.strip()]

for email in emails:
    url = API_URL.format(email)
    headers = {
        'hibp-api-key': API_KEY,
        'user-agent': USER_AGENT
    }
    params = {
        'truncateResponse': 'false'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        breaches = response.json()
        for breach in breaches:
            output = {
                'Name': breach.get('Name'),
                'Title': breach.get('Title'),
                'BreachDate': breach.get('BreachDate'),
                'Description': breach.get('Description'),
                'DataClasses': breach.get('DataClasses')
            }
            print(json.dumps({email: output}, indent=2))
    elif response.status_code == 404:
        # No breach found for this email, do nothing or print a message if desired
        pass
    else:
        print(f"Error checking {email}: {response.status_code} {response.text}")
    # Respect HIBP rate limiting: 1.5 seconds between requests is recommended
    time.sleep(1.6)
```

## What to do:
1. Replace 'YOUR_HIBP_API_KEY' with your actual Have I Been Pwned API key.
2. Replace 'YourAppName/1.0' with your app or script name.
3. Place your list of emails in a file named emails.txt (one email per line).
4. Run the script. For each compromised email, the script outputs the requested breach details in JSON format.

## Notes:
1. The script respects HIBP's rate limiting recommendation by waiting at least 1.6 seconds between requests
2. If an email is not found in any breach, no output is produced for that email.
3. You can modify the script to handle errors or change output formatting as needed.

This approach follows the API documentation requirements for authentication, user agent, and endpoint usage

## Modification
Output the results to Excel

## Script
```
import requests
import time
from openpyxl import Workbook

# Hardcode your API key here
API_KEY = 'YOUR_HIBP_API_KEY'
USER_AGENT = 'YourAppName/1.0'  # Change this to the name of your app/script

INPUT_FILE = 'emails.txt'
OUTPUT_FILE = 'hibp_results.xlsx'
API_URL = 'https://haveibeenpwned.com/api/v3/breachedaccount/{}'

# Read email addresses from file
with open(INPUT_FILE, 'r') as f:
    emails = [line.strip() for line in f if line.strip()]

# Prepare Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "HIBP Results"
ws.append(['Email', 'Name', 'Title', 'BreachDate', 'Description', 'DataClasses'])

for email in emails:
    url = API_URL.format(email)
    headers = {
        'hibp-api-key': API_KEY,
        'user-agent': USER_AGENT
    }
    params = {
        'truncateResponse': 'false'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        breaches = response.json()
        for breach in breaches:
            ws.append([
                email,
                breach.get('Name', ''),
                breach.get('Title', ''),
                breach.get('BreachDate', ''),
                breach.get('Description', ''),
                ', '.join(breach.get('DataClasses', []))
            ])
    elif response.status_code == 404:
        # No breach found for this email, do nothing or add a row if desired
        pass
    else:
        print(f"Error checking {email}: {response.status_code} {response.text}")
    # Respect HIBP rate limiting
    time.sleep(1.6)

# Save Excel file
wb.save(OUTPUT_FILE)
print(f"Results saved to {OUTPUT_FILE}")
```

You will need to install this library
```
pip3 install openpyxl
```

Same instructions as above, this will output to an Excel file called hibp_output.xlsx
