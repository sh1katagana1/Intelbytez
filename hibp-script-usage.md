# Have I Been Pwned Check

## Goal
To create a script that utilizes the Have I Been Pwned api to search for breached accounts via email addresses. Have the script allow me to pass in a list of email addresses via a text file separated by newlines. Have it let me enter my api key in as well via a prompt.

## Language
Python

## Script
```
import requests
import time

def main():
    # Prompt for API key and input file
    api_key = input("Enter your Have I Been Pwned API key: ").strip()
    filename = input("Enter the path to your email list file: ").strip()
    user_agent = "HIBP-Email-Checker/1.0 (your_email@example.com)"  # Customize this

    # Read email addresses
    with open(filename, "r") as f:
        emails = [line.strip() for line in f if line.strip()]

    # API endpoint
    url_template = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"

    for email in emails:
        url = url_template.format(email)
        headers = {
            "hibp-api-key": api_key,
            "user-agent": user_agent
        }
        params = {
            "truncateResponse": "false"
        }
        print(f"\nChecking: {email}")
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                breaches = response.json()
                print(f"  Pwned in {len(breaches)} breach(es):")
                for breach in breaches:
                    print(f"    - {breach['Name']} (Date: {breach['BreachDate']})")
            elif response.status_code == 404:
                print("  Good news — no pwnage found!")
            elif response.status_code == 401:
                print("  Error: Unauthorized (check your API key).")
                break
            else:
                print(f"  Error: Received status code {response.status_code} - {response.text}")
        except Exception as e:
            print(f"  Exception occurred: {e}")
        # Respect the API's rate limit of 1 request per 1.5 seconds
        time.sleep(1.6)

if __name__ == "__main__":
    main()
```

## How to use
1. Save your email addresses in a text file, one per line.
2. Run the script. It will prompt for your API key and the path to your email file.
3. The script will output the breach status for each email.

Notes:
1. You must provide your own API key and set a meaningful user agent as required by the API
2. The script sleeps for 1.6 seconds between requests to comply with rate limits
3. The script checks each email individually, as bulk search is not available unless you own the domain

## Modification 1
I want to hardcode my API key into the script to not get prompted for it.

## Script
```
import requests
import time

# === CONFIGURATION ===
API_KEY = "YOUR_API_KEY_HERE"  # <-- Put your HIBP API key here
USER_AGENT = "HIBP-Email-Checker/1.0 (your_email@example.com)"  # Customize this
EMAIL_LIST_FILE = "emails.txt"  # Default file name (edit as needed)
# =====================

def main():
    # Read email addresses
    try:
        with open(EMAIL_LIST_FILE, "r") as f:
            emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{EMAIL_LIST_FILE}' not found.")
        return

    url_template = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"

    for email in emails:
        url = url_template.format(email)
        headers = {
            "hibp-api-key": API_KEY,
            "user-agent": USER_AGENT
        }
        params = {
            "truncateResponse": "false"
        }
        print(f"\nChecking: {email}")
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                breaches = response.json()
                print(f"  Pwned in {len(breaches)} breach(es):")
                for breach in breaches:
                    print(f"    - {breach['Name']} (Date: {breach['BreachDate']})")
            elif response.status_code == 404:
                print("  Good news — no pwnage found!")
            elif response.status_code == 401:
                print("  Error: Unauthorized (check your API key).")
                break
            else:
                print(f"  Error: Received status code {response.status_code} - {response.text}")
        except Exception as e:
            print(f"  Exception occurred: {e}")
        # Respect the API's rate limit of 1 request per 1.5 seconds
        time.sleep(1.6)

if __name__ == "__main__":
    main()
```

## How to use
1. Replace YOUR_API_KEY_HERE with your actual Have I Been Pwned API key.
2. Optionally, change EMAIL_LIST_FILE to the path of your email list file, or keep it as emails.txt.
3. Run the script. No prompts for API key will appear.

## Modification 2
Output the results to Excel

## Script
```
import requests
import time
from openpyxl import Workbook

# === CONFIGURATION ===
API_KEY = "YOUR_API_KEY_HERE"  # <-- Put your HIBP API key here
USER_AGENT = "HIBP-Email-Checker/1.0 (your_email@example.com)"  # Customize this
EMAIL_LIST_FILE = "emails.txt"  # Default file name (edit as needed)
OUTPUT_FILE = "results.xlsx"
# =====================

def main():
    # Read email addresses
    try:
        with open(EMAIL_LIST_FILE, "r") as f:
            emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{EMAIL_LIST_FILE}' not found.")
        return

    url_template = "https://haveibeenpwned.com/api/v3/breachedaccount/{}"

    # Set up Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "HIBP Results"
    ws.append([
        "Email",
        "Breached?", 
        "Breach Count", 
        "Breach Names", 
        "Breach Dates"
    ])

    for email in emails:
        url = url_template.format(email)
        headers = {
            "hibp-api-key": API_KEY,
            "user-agent": USER_AGENT
        }
        params = {
            "truncateResponse": "false"
        }
        print(f"\nChecking: {email}")
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                breaches = response.json()
                breach_names = ", ".join(b['Name'] for b in breaches)
                breach_dates = ", ".join(b['BreachDate'] for b in breaches)
                ws.append([
                    email,
                    "YES",
                    len(breaches),
                    breach_names,
                    breach_dates
                ])
                print(f"  Pwned in {len(breaches)} breach(es).")
            elif response.status_code == 404:
                ws.append([email, "NO", 0, "", ""])
                print("  Good news — no pwnage found!")
            elif response.status_code == 401:
                print("  Error: Unauthorized (check your API key).")
                break
            else:
                ws.append([email, "ERROR", "", "", f"Status {response.status_code}"])
                print(f"  Error: Received status code {response.status_code} - {response.text}")
        except Exception as e:
            ws.append([email, "ERROR", "", "", str(e)])
            print(f"  Exception occurred: {e}")
        # Respect the API's rate limit of 1 request per 1.5 seconds
        time.sleep(1.6)

    # Save results to Excel
    wb.save(OUTPUT_FILE)
    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
```

## Notes
You will need to install:
```
pip install openpyxl
```
## How it works
1. Each email is checked and the results are written to an Excel file.
2. The Excel file will have columns: Email, Breached?, Breach Count, Breach Names, Breach Dates.
3. Errors (e.g., API errors) are also recorded in the file.

## Customization
1. Change the OUTPUT_FILE variable if you want a different filename.
2. You can adjust the Excel columns as needed.

