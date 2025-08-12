import requests
from bs4 import BeautifulSoup

def load_keywords(filepath):
    """Load keyword phrases from a file, one per line."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_recent_victims():
    """Fetch the RansomLook recent victims page and extract the entries."""
    url = 'https://www.ransomlook.io/recent'
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    entries = []
    if table:
        # Each row: Date, Title, Group
        for row in table.find_all('tr')[1:]:  # skip possible header
            cols = row.find_all('td')
            if len(cols) >= 3:
                date = cols[0].get_text(strip=True)
                title = cols[1].get_text(strip=True)
                group = cols[2].get_text(strip=True)
                entries.append({'date': date, 'title': title, 'group': group})
    else:
        print("Unable to locate the table of recent posts. The page structure may have changed.")
    return entries

def find_matches(keywords, entries):
    """Yield matches where keyword phrase (exact, case-insensitive) is found in title."""
    matches = []
    for kw in keywords:
        lower_kw = kw.lower()
        for entry in entries:
            if lower_kw in entry['title'].lower():
                matches.append({'keyword': kw, **entry})
    return matches

def main(keywords_file):
    keywords = load_keywords(keywords_file)
    print(f"Loaded {len(keywords)} keywords.")

    entries = fetch_recent_victims()
    print(f"Fetched {len(entries)} recent victim entries.")

    matches = find_matches(keywords, entries)
    if matches:
        print("\nMatches found:")
        for m in matches:
            print(f"Keyword: \"{m['keyword']}\"  — Date: {m['date']}, Victim: \"{m['title']}\", Group: {m['group']}")
    else:
        print("No matches found.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_ransomlook.py <keywords_file>")
        sys.exit(1)
    main(sys.argv[1])
