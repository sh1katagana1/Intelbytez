# Favicon Hash Generator

***

## Goal
To utilize Shodan to look for any sites using our favicon hash, it is important to generate the favicon hash just like Shodan does. I need to create a script that prompts me for a text file list of URLs, then does the following:
1. Fetch the HTML of the page.
2. Parse it for <link rel="icon" ...> or similar tags.
3. Use the href from that tag to locate the actual favicon.
4. Fall back to /favicon.ico if no tag is found.
5. Create the favicon
6. Export as an Excel file.

## Language
Python

## Dependencies
```
pip3 install requests mmh3 openpyxl beautifulsoup4
```
Create a text file list of URLs called urls.txt, then run this script:

## Script
```
import requests
import mmh3
import base64
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime

def find_favicon_url(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link and icon_link.get("href"):
            favicon_href = icon_link["href"]
            favicon_url = urljoin(base_url, favicon_href)
            return favicon_url
    except Exception as e:
        print(f"[!] Could not parse HTML for {base_url}: {e}")
    return urljoin(base_url, "/favicon.ico")  # fallback

def get_favicon_hash(url):
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'http://' + url
            parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        favicon_url = find_favicon_url(base_url)
        print(f"[+] Fetching favicon from: {favicon_url}")
        response = requests.get(favicon_url, timeout=10)
        response.raise_for_status()

        favicon_data = base64.encodebytes(response.content)
        hash_val = mmh3.hash(favicon_data)
        print(f"[✓] {base_url} → mmh3 hash: {hash_val}")
        return base_url, favicon_url, hash_val

    except requests.RequestException as e:
        print(f"[✗] Error fetching favicon from {url}: {e}")
    except Exception as e:
        print(f"[✗] Unexpected error with {url}: {e}")
    return url, None, None

def save_to_excel(data, filename='favicon_hashes.xlsx'):
    wb = Workbook()
    ws = wb.active
    ws.title = "Favicon Hashes"
    ws.append(["Input URL", "Favicon URL", "mmh3 Hash", "Timestamp"])

    for entry in data:
        base_url, favicon_url, hash_val = entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append([base_url, favicon_url, hash_val, timestamp])

    wb.save(filename)
    print(f"\n[✓] Results saved to {filename}")

def main():
    input_file = input("Enter the path to your URL list (e.g., urls.txt): ").strip()
    try:
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[✗] File not found: {input_file}")
        return

    results = []
    for url in urls:
        result = get_favicon_hash(url)
        if result[2] is not None:
            results.append(result)

    if results:
        save_to_excel(results)
    else:
        print("[!] No valid favicon hashes found.")

if __name__ == '__main__':
    main()
```
