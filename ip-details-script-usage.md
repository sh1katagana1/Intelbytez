# IP Details Check Script Usage

***

## Goal
To get prompted for an IP address and then have the script get data from the following and not require an API key for any of them:
1. Reverse ip check
2. IP details from ip-api.com
3. IP details from ipinfo.io
4. ARIN details
5. Tor relay check
6. Whois check
7. Blacklist check amongst common lists
8. Port scan for common ports.

## Language
Python

## Script
```
import ipaddress
import socket
import requests
from ipwhois import IPWhois

DNSBLS = [
    "zen.spamhaus.org",
    "bl.spamcop.net",
    "dnsbl.sorbs.net",
    "b.barracudacentral.org",
    "psbl.surriel.com",
    "cbl.abuseat.org",
    "dnsbl-1.uceprotect.net",
    "dnsbl-2.uceprotect.net",
    "dnsbl-3.uceprotect.net",
    "hostkarma.junkemailfilter.com",
    "spam.abuse.ch",
    "spam.dnsbl.sorbs.net",
    "ubl.unsubscore.com"
]

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3389]

def print_divider():
    print('-' * 50)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def reverse_lookup(ip):
    try:
        domain = socket.gethostbyaddr(ip)
        return domain[0]
    except socket.herror:
        return None

def get_ip_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data['status'] == 'success':
            return {
                'country': data.get('country'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'isp': data.get('isp')
            }
        else:
            return None
    except Exception:
        return None

def get_ip_details_ipinfo(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return {
            'ip': data.get('ip'),
            'hostname': data.get('hostname'),
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'loc': data.get('loc'),
            'org': data.get('org'),
            'postal': data.get('postal'),
            'timezone': data.get('timezone')
        }
    except Exception:
        return None

def get_arin_rdap(ip):
    try:
        url = f"https://rdap.arin.net/registry/ip/{ip}"
        response = requests.get(url, timeout=10)
        data = response.json()
        network = data.get('name', 'N/A')
        handle = data.get('handle', 'N/A')
        start_address = data.get('startAddress', 'N/A')
        end_address = data.get('endAddress', 'N/A')
        org = data.get('org', {}).get('name', 'N/A') if data.get('org') else 'N/A'
        country = data.get('country', 'N/A')
        remarks = data.get('remarks', [])
        description = remarks[0]['description'][0] if remarks else 'N/A'
        return {
            'Network': network,
            'Handle': handle,
            'Start Address': start_address,
            'End Address': end_address,
            'Organization': org,
            'Country': country,
            'Description': description
        }
    except Exception:
        return None

def check_tor_relay(ip):
    try:
        url = f"https://onionoo.torproject.org/details?search={ip}"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('relays'):
            return True
        return False
    except Exception:
        return False

def whois_lookup(ip):
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap()
        result = {
            'asn': res.get('asn'),
            'asn_description': res.get('asn_description'),
            'network_name': res['network'].get('name'),
            'country': res['network'].get('country'),
            'cidr': res['network'].get('cidr'),
            'org': res['network'].get('org'),
            'emails': ', '.join(res['network'].get('emails', [])) if res['network'].get('emails') else 'N/A'
        }
        return result
    except Exception:
        return None

def check_dnsbl(ip):
    try:
        reversed_ip = '.'.join(reversed(ip.split('.')))
    except Exception:
        return []
    blacklisted = []
    for dnsbl in DNSBLS:
        query = f"{reversed_ip}.{dnsbl}"
        try:
            socket.gethostbyname(query)
            blacklisted.append(dnsbl)
        except socket.gaierror:
            continue
    return blacklisted

def port_scan(ip, ports, timeout=1):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
            except Exception:
                continue
    return open_ports

if __name__ == "__main__":
    ip = input("Enter an IP address: ").strip()
    if not is_valid_ip(ip):
        print("Invalid IP address.")
    else:
        # Reverse DNS Lookup
        print_divider()
        result = reverse_lookup(ip)
        if result:
            print(f"Domain name for {ip}: {result}")
        else:
            print(f"No PTR record found for {ip}.")

        # IP Location Lookup (ip-api.com)
        print_divider()
        location = get_ip_location(ip)
        if location:
            print(f"Location info from ip-api.com for {ip}:")
            print(f"  Country: {location['country']}")
            print(f"  Region: {location['region']}")
            print(f"  City: {location['city']}")
            print(f"  Latitude: {location['lat']}")
            print(f"  Longitude: {location['lon']}")
            print(f"  ISP: {location['isp']}")
        else:
            print("Could not retrieve location information from ip-api.com.")

        # IP Details from ipinfo.io
        print_divider()
        ipinfo = get_ip_details_ipinfo(ip)
        if ipinfo:
            print(f"IP details from ipinfo.io for {ip}:")
            for k, v in ipinfo.items():
                print(f"  {k.capitalize()}: {v}")
        else:
            print("Could not retrieve details from ipinfo.io.")

        # ARIN RDAP Lookup
        print_divider()
        arin = get_arin_rdap(ip)
        if arin:
            print(f"ARIN RDAP details for {ip}:")
            for k, v in arin.items():
                print(f"  {k}: {v}")
        else:
            print("Could not retrieve ARIN RDAP details.")

        # Tor Relay Check
        print_divider()
        if check_tor_relay(ip):
            print(f"{ip} is a Tor relay node.")
        else:
            print(f"{ip} is NOT a Tor relay node.")

        # WHOIS Lookup
        print_divider()
        whois_info = whois_lookup(ip)
        if whois_info:
            print(f"WHOIS info for {ip}:")
            print(f"  ASN: {whois_info['asn']}")
            print(f"  ASN Description: {whois_info['asn_description']}")
            print(f"  Network Name: {whois_info['network_name']}")
            print(f"  Country: {whois_info['country']}")
            print(f"  CIDR: {whois_info['cidr']}")
            print(f"  Org: {whois_info['org']}")
            print(f"  Emails: {whois_info['emails']}")
        else:
            print("Could not retrieve WHOIS information.")

        # DNSBL Blacklist Check
        print_divider()
        blacklists = check_dnsbl(ip)
        if blacklists:
            print(f"{ip} is blacklisted on the following DNSBLs:")
            for bl in blacklists:
                print(f"  - {bl}")
        else:
            print(f"{ip} is NOT blacklisted on the tested DNSBLs.")

        # Port Scan
        print_divider()
        print("Performing port scan on common ports...")
        open_ports = port_scan(ip, COMMON_PORTS)
        if open_ports:
            print(f"Open ports on {ip}: {', '.join(str(p) for p in open_ports)}")
        else:
            print(f"No common ports open on {ip}.")
        print_divider()
```

## Reverse IP Lookup Notes
1. The script asks for an IP address.
2. It checks if the IP is valid using the ipaddress module.
3. If valid, it attempts a reverse DNS lookup using socket.gethostbyaddr.
4. If a PTR record exists, it prints the domain name; otherwise, it notifies you that no record was found

## IP-api.com Notes
To get the geographical location of an IP address, you’ll need to use an external IP geolocation service. A popular and free one is ip-api.com. You can query their API with a simple HTTP request and parse the result.

## Tor Relay Check Notes
The script queries the Onionoo API (https://onionoo.torproject.org/details?search=<ip>) to see if the IP is listed as a Tor relay. This is the same backend used by the Tor Metrics relay search page.

## Whois Check Notes
For WHOIS lookups in Python, the most common library is python-whois for domains, but for IP addresses, ipwhois is more appropriate. You will need this library:
```
pip3 install requests ipwhois
```

## BlackList Check Notes
IPVoid, like other blacklist checkers, queries public DNSBLs (DNS-based Blackhole Lists). You can perform the same checks directly—this is reliable, ethical, and doesn’t require an API key. This script mimics what IPVoid does—checking major DNSBLs. This is the industry standard and is what IPVoid does behind the scenes.

## Arin Check Notes
ARIN provides a public RDAP (Registration Data Access Protocol) endpoint for IP address lookups. You can query it directly

## Port Scan Check Notes
Adds a simple port scan using Python’s socket module to your script. This will check if the following common ports are open on the given IP:
```
    21 (FTP)

    22 (SSH)

    23 (Telnet)

    25 (SMTP)

    53 (DNS)

    80 (HTTP)

    110 (POP3)

    143 (IMAP)

    443 (HTTPS)

    3389 (RDP)
```








