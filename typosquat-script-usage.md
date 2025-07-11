# Typosquat Script

***


## Goal
To create a script that takes in a list of domain names via text file, permutates them as typical typosquatting would do and check them against the newly registered domains list for the past 24 hours

## Language
Python

## Script
```
import subprocess
import sys

def generate_permutations(domain):
    # Use dnstwist to generate permutations, output as CSV
    result = subprocess.run(
        ['dnstwist', '--format', 'csv', domain],
        capture_output=True, text=True
    )
    lines = result.stdout.splitlines()
    # Skip header, extract domain names
    permutations = [line.split(',')[0] for line in lines[1:] if line]
    return set(permutations)

def load_domains_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def load_newly_registered_domains(filename):
    with open(filename, 'r') as f:
        return set(line.strip().lower() for line in f if line.strip())

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python typosquat_check.py domains.txt newly_registered_domains.txt")
        sys.exit(1)

    domains_file = sys.argv[1]
    nrd_file = sys.argv[2]

    domains = load_domains_from_file(domains_file)
    nrd_set = load_newly_registered_domains(nrd_file)
    found = {}

    for domain in domains:
        permutations = generate_permutations(domain)
        matches = permutations & nrd_set
        if matches:
            found[domain] = matches

    for domain, matches in found.items():
        print(f"\nPossible typosquatting domains for {domain} found in NRD list:")
        for match in matches:
            print(f"  - {match}")
```

## How to use
1. Install dnstwist:
```
pip install dnstwist
```
2. Create a file called domains.txt. This is a list of domains to monitor (one per line).
3. Create a file called newly_registered_domains.txt: Download the most recent 24-hour NRD file from a provider such as domains-monitor.com, or whoisds.com. The whoisds.com lets you download just the domains list for free, as opposed to full whois info for a fee: https://www.whoisds.com/newly-registered-domains grab that list each day and name it newly_registered_domains.txt
2. Run the script (assuming you called the script typosquat_check.py):
```
python typosquat_check.py domains.txt newly_registered_domains.txt
```
## Notes
1. This script uses dnstwist to generate typosquatting permutations. 
2. It checks each permutation against the set of newly registered domains from the last 24 hours
3. Alternative tools for permutation generation include ail-typo-squatting, which can be substituted for dnstwist if preferred.

It seems that there is a couple of free feeds where some tools get their newly registered domains list, but the one I see the most is https://www.whoisds.com/newly-registered-domains Additionally, there is a phishing domain discovered list daily at https://github.com/Phishing-Database/Phishing.Database 

This bash script will download and concatenate the past 7 days worth of NRD data rom whoisds: https://github.com/PeterDaveHello/nrd-list-downloader/blob/master/nrd-list-downloader.sh 

Another source pulling from ICANN data is https://codeberg.org/webamon/newly_registered_domains

An alternative that uses the DNSTwist algorithm is DNSRazzle https://github.com/f8al/DNSrazzle   This will do the permutations via the DNSTwist algorithm, then check if they are registered. It also does screenshots of ones it finds and a comparison check to the original website. It outputs to Excel so even though it pulls all data throughout the years, it does let you filter for things like year and month. It doesn't seem to be the most recent stuff but the past month is the latest it has. 

