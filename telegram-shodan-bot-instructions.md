# Telegram Shodan Bot

***

## Goal
I want to create a local self hosted telegram bot that lets me do /domain and a domain name and it looks up details about it in Shodan. Let me be able to hardcode my API key in the script. Have it output in the bot channel the details about the domain. Additionally, put in one for /ip then an ip address that looks up the IP in Shodan and gives me details about it

Here is a high-level approach including a sample Python script using python-telegram-bot and the official shodan Python library.
1. Get your Shodan API key and Telegram Bot Token (from BotFather).
2. Install required libraries: pip install python-telegram-bot shodan
3. Hardcode your Shodan API key in the script.
4. Write handlers for /domain and /ip commands.
5. Use Shodan API's host() method for IP lookup and search() method with domain query for domain lookup.
6. Respond with formatted results back in your Telegram bot chat/channel.

## Language
Python

## Script
```
import shodan
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Hardcoded keys (replace these with your actual keys)
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize Shodan client
api = shodan.Shodan(SHODAN_API_KEY)

async def domain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /domain <domain_name>")
        return
    domain = context.args[0]
    try:
        # Search Shodan for hostname matching domain
        results = api.search(f'hostname:{domain}')
        if results['matches']:
            reply = f"Results for domain {domain}:\n"
            for match in results['matches'][:5]:  # limit to first 5
                ip = match.get('ip_str', 'N/A')
                port = match.get('port', 'N/A')
                org = match.get('org', 'N/A')
                product = match.get('product', '')
                reply += f"- IP: {ip}, Port: {port}, Org: {org}, Product: {product}\n"
        else:
            reply = f"No results found for domain {domain}."
    except shodan.APIError as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ip <ip_address>")
        return
    ip = context.args[0]
    try:
        host = api.host(ip)
        reply = f"IP: {ip}\n"
        reply += f"Org: {host.get('org', 'N/A')}\n"
        reply += f"Location: {host.get('city', 'N/A')}, {host.get('country_name', 'N/A')}\n"
        ports = ', '.join(str(port) for port in host.get('ports', []))
        reply += f"Open Ports: {ports}\n"
        # Optional banner info on first 3 services
        for service in host.get('data', [])[:3]:
            banner = service.get('data', '').strip()
            port = service.get('port', 'N/A')
            reply += f"\nPort {port} banner:\n{banner}\n"
    except shodan.APIError as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("domain", domain_command))
    application.add_handler(CommandHandler("ip", ip_command))

    application.run_polling()

if __name__ == '__main__':
    main()
```

1. Replace 'YOUR_SHODAN_API_KEY' and 'YOUR_TELEGRAM_BOT_TOKEN' with your actual keys.
2. This example uses polling; you can also set up webhooks if desired.
3. The /domain command queries Shodan with a hostname filter.
4. The /ip command directly looks up a host by IP.

This way you can self-host the bot locally, it accepts commands for domain and IP, queries Shodan, and sends details back in the Telegram bot chat.

## How to use this script:
1. Replace 'YOUR_SHODAN_API_KEY' and 'YOUR_TELEGRAM_BOT_TOKEN' with your actual keys.
2. Make sure you have python-telegram-bot v20+ installed:
```
pip install python-telegram-bot --upgrade
pip install shodan
```
Run the script locally:

```
python shodanbot.py
```
Use /domain example.com or /ip 8.8.8.8 in your Telegram bot chat.

## Modification 1
Is there a way to get more details from Shodan about the domains and the IPs? There are ways to retrieve more detailed information from Shodan for both domain and IP lookups by using additional data fields, filters, and advanced search parameters available in the Shodan API.
For IP Addresses (host() method) the Shodan host() method returns rich information including:

1. Organization (org)
2. Location (city, country)
3. List of open ports
4. Service banners for each port (e.g., HTTP headers, SSH version)
5. Operating system information (if available)
6. Vulnerabilities and CVE data (if enabled with your API key)
7. Autonomous System Number (ASN)
8. Hostnames and domains associated

You can extract and display these extra fields in your bot's reply to get a more comprehensive overview.

For Domain Searches (search() method with hostname: filter)

1. You can refine the search using filters such as hostname:<domain>, and get multiple results of IPs and services related to that domain.
2. The results include fields like IP, port, organization, product (software detected), OS, location, tags, and potentially vulnerabilities.
3. You can customize your query further with additional filters, like by country, port, or product.
4. You can fetch more results or paginate through them if needed, but that uses Shodan query credits.

Additional ways to enhance detail in your queries:

1. Use facets: To get summary information about properties like top countries or ports in the result set.
2. Fetch banners: The raw data/banners often include HTTP headers, SSH versions, SSL cert info, etc.
3. Search with filters: For example ssl.cert.subject.cn:<domain>, product:nginx, country:US.
4. Get vulnerability info: If you have access, fields like vulns expose known CVEs for the host.

Example fields you can add to your bot output for more detail:

1. Hostnames on the IP
2. Operating system (os)
3. ASN (asn)
4. Organization (org)
5. Country and city
6. Open ports with banners (service details)
7. Tag and module info like product, version
8. Vulnerabilities (e.g., vulns field listing known CVEs)

By expanding your bot’s handlers to extract these additional fields from Shodan API responses (both from host() results for IP and from search() matches for domain queries), you can provide a significantly richer set of details.


Let's modify the script to give me the absolute most details Shodan can give about the domain or ip

```
import shodan
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import textwrap

# Hardcoded keys (replace these with your actual keys)
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize Shodan client
api = shodan.Shodan(SHODAN_API_KEY)

def format_service_banner(service):
    # Show port, transport, product/version info, tags, vuln info, banner data (limit length)
    port = service.get('port', 'N/A')
    transport = service.get('transport', 'N/A')
    product = service.get('product', '')
    version = service.get('version', '')
    extra = f"{product} {version}".strip()
    tags = service.get('tags', [])
    vulns = service.get('vulns', {})
    banner_data = service.get('data', '').strip()
    # Limit banner data length for Telegram readability
    banner_data = (banner_data[:500] + '...') if len(banner_data) > 500 else banner_data

    banner_text = f"Port: {port}/{transport}\n"
    if extra:
        banner_text += f"Product: {extra}\n"
    if tags:
        banner_text += f"Tags: {', '.join(tags)}\n"
    if vulns:
        banner_text += f"Vulnerabilities: {', '.join(vulns.keys())}\n"
    banner_text += f"Banner:\n{textwrap.indent(banner_data, '  ')}\n"
    return banner_text

async def domain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /domain <domain_name>")
        return
    domain = context.args[0]
    try:
        # Fetch up to 10 results, minified=False for full banners
        results = api.search(f"hostname:{domain}", minify=False)
        total = results.get('total', 0)
        if total == 0:
            reply = f"No results found for domain {domain}."
        else:
            reply = [f"Found {total} results for domain {domain}, showing up to 5:\n"]
            for match in results['matches'][:5]:
                ip = match.get('ip_str', 'N/A')
                org = match.get('org', 'N/A')
                asn = match.get('asn', 'N/A')
                os = match.get('os', 'N/A')
                location = f"{match.get('city', 'N/A')}, {match.get('country_name', 'N/A')}"
                ports = ", ".join(str(p) for p in match.get('ports', []))
                hostnames = ", ".join(match.get('hostnames', []))
                timestamp = match.get('timestamp', 'N/A')
                tags = ", ".join(match.get('tags', []))
                vulns = match.get('vulns', {})
                
                reply.append(f"IP: {ip}")
                reply.append(f"Org: {org}")
                reply.append(f"ASN: {asn}")
                reply.append(f"OS: {os}")
                reply.append(f"Location: {location}")
                reply.append(f"Open ports: {ports}")
                if hostnames:
                    reply.append(f"Hostnames: {hostnames}")
                if tags:
                    reply.append(f"Tags: {tags}")
                if vulns:
                    reply.append(f"Vulnerabilities: {', '.join(vulns.keys())}")
                reply.append(f"First seen: {timestamp}")

                # Show banner snippet (limit length)
                banner_data = match.get('data', '').strip()
                if banner_data:
                    banner_data = (banner_data[:700] + '...') if len(banner_data) > 700 else banner_data
                    reply.append(f"Banner:\n{banner_data}")
                reply.append("-" * 40)

            reply = "\n".join(reply)
    except shodan.APIError as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ip <ip_address>")
        return
    ip = context.args[0]
    try:
        # Get full host info with history and all banners
        host = api.host(ip, history=True, minify=False)

        reply = [
            f"IP: {ip}",
            f"Org: {host.get('org', 'N/A')}",
            f"ASN: {host.get('asn', 'N/A')}",
            f"OS: {host.get('os', 'N/A')}",
            f"Hostnames: {', '.join(host.get('hostnames', [])) or 'N/A'}",
            f"Location: {host.get('city', 'N/A')}, {host.get('country_name', 'N/A')}",
            f"Number of open ports: {len(host.get('ports', []))}",
            f"Open ports: {', '.join(str(port) for port in host.get('ports', []))}",
            f"Last update: {host.get('last_update', 'N/A')}",
        ]

        # Vulnerabilities at host level (if any)
        vulns = host.get('vulns', {})
        if vulns:
            reply.append(f"Vulnerabilities: {', '.join(vulns.keys())}")

        # Show banners from current data
        reply.append("\n=== Current Service Banners (up to 5) ===")
        for service in host.get('data', [])[:5]:
            reply.append(format_service_banner(service))
            reply.append("-" * 30)

        # Optionally, show historical banners with timestamps
        if 'history' in host and host['history']:
            reply.append("\n=== Historical Service Banners (up to 3) ===")
            # Showing up to 3 historical banner sets
            for i, hist in enumerate(host['history'][:3]):
                ts = hist.get('timestamp', 'N/A')
                reply.append(f"\n--- History entry {i+1}: {ts} ---")
                for service in hist.get('data', [])[:3]:
                    reply.append(format_service_banner(service))
                reply.append("-" * 30)

        reply = "\n".join(reply)
    except shodan.APIError as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("domain", domain_command))
    application.add_handler(CommandHandler("ip", ip_command))

    application.run_polling()

if __name__ == '__main__':
    main()
```
## Key improvements:

1. host(ip, history=True, minify=False) fetches current and historical host data with full banners.
2. search(..., minify=False) fetches full banner data without truncation on domain search.
3. Added detailed output including organization, ASN, OS, hostnames, location, tags, vulnerabilities, timestamps.
4. Displays banner data snippets from services and historical entries.
5. Limits text length per banner to keep Telegram messages readable.
6. Shows multiple matched results up to 5 for domain.

Make sure your API key has sufficient query credits as these detailed requests consume more quota

## Modification 2
I want to modify the script so it includes intro text when the bot starts. Have it say "Thank you for checking out my shodan bot. Type in /domain <domain name> for info about a domain. Type /ip <Ip address> for info about an ip address. "

```
import shodan
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import textwrap

# Hardcoded keys (replace these with your actual keys)
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize Shodan client
api = shodan.Shodan(SHODAN_API_KEY)

def format_service_banner(service):
    port = service.get('port', 'N/A')
    transport = service.get('transport', 'N/A')
    product = service.get('product', '')
    version = service.get('version', '')
    extra = f"{product} {version}".strip()
    tags = service.get('tags', [])
    vulns = service.get('vulns', {})
    banner_data = service.get('data', '').strip()
    banner_data = (banner_data[:500] + '...') if len(banner_data) > 500 else banner_data

    banner_text = f"Port: {port}/{transport}\n"
    if extra:
        banner_text += f"Product: {extra}\n"
    if tags:
        banner_text += f"Tags: {', '.join(tags)}\n"
    if vulns:
        banner_text += f"Vulnerabilities: {', '.join(vulns.keys())}\n"
    banner_text += f"Banner:\n{textwrap.indent(banner_data, '  ')}\n"
    return banner_text

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "Thank you for checking out my Shodan bot.\n"
        "Type /domain <domain name> for info about a domain.\n"
        "Type /ip <ip address> for info about an IP address."
    )
    await update.message.reply_text(intro_text)

async def domain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /domain <domain_name>")
        return
    domain = context.args[0]
    try:
        results = api.search(f"hostname:{domain}", minify=False)
        total = results.get('total', 0)
        if total == 0:
            reply = f"No results found for domain {domain}."
        else:
            reply = [f"Found {total} results for domain {domain}, showing up to 5:\n"]
            for match in results['matches'][:5]:
                ip = match.get('ip_str', 'N/A')
                org = match.get('org', 'N/A')
                asn = match.get('asn', 'N/A')
                os = match.get('os', 'N/A')
                location = f"{match.get('city', 'N/A')}, {match.get('country_name', 'N/A')}"
                ports = ", ".join(str(p) for p in match.get('ports', []))
                hostnames = ", ".join(match.get('hostnames', []))
                timestamp = match.get('timestamp', 'N/A')
                tags = ", ".join(match.get('tags', []))
                vulns = match.get('vulns', {})

                reply.append(f"IP: {ip}")
                reply.append(f"Org: {org}")
                reply.append(f"ASN: {asn}")
                reply.append(f"OS: {os}")
                reply.append(f"Location: {location}")
                reply.append(f"Open ports: {ports}")
                if hostnames:
                    reply.append(f"Hostnames: {hostnames}")
                if tags:
                    reply.append(f"Tags: {tags}")
                if vulns:
                    reply.append(f"Vulnerabilities: {', '.join(vulns.keys())}")
                reply.append(f"First seen: {timestamp}")

                banner_data = match.get('data', '').strip()
                if banner_data:
                    banner_data = (banner_data[:700] + '...') if len(banner_data) > 700 else banner_data
                    reply.append(f"Banner:\n{banner_data}")
                reply.append("-" * 40)

            reply = "\n".join(reply)
    except shodan.APIError as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ip <ip_address>")
        return
    ip = context.args[0]
    try:
        host = api.host(ip, history=True, minify=False)

        reply = [
            f"IP: {ip}",
            f"Org: {host.get('org', 'N/A')}",
            f"ASN: {host.get('asn', 'N/A')}",
            f"OS: {host.get('os', 'N/A')}",
            f"Hostnames: {', '.join(host.get('hostnames', [])) or 'N/A'}",
            f"Location: {host.get('city', 'N/A')}, {host.get('country_name', 'N/A')}",
            f"Number of open ports: {len(host.get('ports', []))}",
            f"Open ports: {', '.join(str(port) for port in host.get('ports', []))}",
            f"Last update: {host.get('last_update', 'N/A')}",
        ]

        vulns = host.get('vulns', {})
        if vulns:
            reply.append(f"Vulnerabilities: {', '.join(vulns.keys())}")

        reply.append("\n=== Current Service Banners (up to 5) ===")
        for service in host.get('data', [])[:5]:
            reply.append(format_service_banner(service))
            reply.append("-" * 30)

        if 'history' in host and host['history']:
            reply.append("\n=== Historical Service Banners (up to 3) ===")
            for i, hist in enumerate(host['history'][:3]):
                ts = hist.get('timestamp', 'N/A')
                reply.append(f"\n--- History entry {i+1}: {ts} ---")
                for service in hist.get('data', [])[:3]:
                    reply.append(format_service_banner(service))
                reply.append("-" * 30)

        reply = "\n".join(reply)
    except shodan.APIError as e:
        reply = f"Error: {e}"
    await update.message.reply_text(reply)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add start command handler
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("domain", domain_command))
    application.add_handler(CommandHandler("ip", ip_command))

    application.run_polling()

if __name__ == '__main__':
    main()
```
## What was added:
1. A new async handler start_command that sends your intro text.
2. Registered /start command handler in the application.

Now, when a user sends /start to your bot, they will receive the welcome message with instructions.

## Modification 3
I want to create a text report in markdown, txt, pdf or html format after it gives the response and have that report be downloadable?

It is possible to generate a detailed report (in Markdown, plain text, HTML, or PDF) after sending the Telegram message response, then provide the user a downloadable file link or send the file directly in the Telegram chat. Here’s how you can do it with my existing Telegram bot:

1. Generate the report content. Use the same data you have in the message, but format it in your preferred file type (.txt, .md, .html, or .pdf).
2. Save the report to a local file. Write the report content to a file on disk.
3. Send the file back to the user in Telegram. Use the Telegram bot API’s send_document method (available via the python-telegram-bot library) to send the file as a document.

Let's do the markdown report and combine it all with the last version of the script I have been making for shodan.

```
python
import shodan
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import textwrap
import tempfile
import os

# Hardcoded keys (replace with your actual keys)
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Initialize Shodan client
api = shodan.Shodan(SHODAN_API_KEY)

def format_service_banner(service):
    port = service.get('port', 'N/A')
    transport = service.get('transport', 'N/A')
    product = service.get('product', '')
    version = service.get('version', '')
    extra = f"{product} {version}".strip()
    tags = service.get('tags', [])
    vulns = service.get('vulns', {})
    banner_data = service.get('data', '').strip()
    banner_data = (banner_data[:500] + '...') if len(banner_data) > 500 else banner_data

    banner_text = f"Port: {port}/{transport}\n"
    if extra:
        banner_text += f"Product: {extra}\n"
    if tags:
        banner_text += f"Tags: {', '.join(tags)}\n"
    if vulns:
        banner_text += f"Vulnerabilities: {', '.join(vulns.keys())}\n"
    banner_text += f"Banner:\n{textwrap.indent(banner_data, '  ')}\n"
    return banner_text

def create_markdown_report(domain_or_ip, title, lines):
    """
    Helper to create markdown content from a list of strings,
    with a title and heading.
    """
    md = f"# Shodan Report for {title}: {domain_or_ip}\n\n"
    for line in lines:
        md += line + "\n\n"
    return md

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro_text = (
        "Thank you for checking out my Shodan bot.\n"
        "Type /domain <domain name> for info about a domain.\n"
        "Type /ip <ip address> for info about an IP address."
    )
    await update.message.reply_text(intro_text)

async def domain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /domain <domain_name>")
        return
    domain = context.args[0]
    tmp_md_filepath = None  # initialize for safety
    try:
        results = api.search(f"hostname:{domain}", minify=False)
        total = results.get('total', 0)
        if total == 0:
            reply = f"No results found for domain {domain}."
            await update.message.reply_text(reply)
            return

        reply_lines = [f"Found {total} results for domain {domain}, showing up to 5:\n"]
        for match in results['matches'][:5]:
            ip = match.get('ip_str', 'N/A')
            org = match.get('org', 'N/A')
            asn = match.get('asn', 'N/A')
            os_ = match.get('os', 'N/A')
            location = f"{match.get('city', 'N/A')}, {match.get('country_name', 'N/A')}"
            ports = ", ".join(str(p) for p in match.get('ports', []))
            hostnames = ", ".join(match.get('hostnames', []))
            timestamp = match.get('timestamp', 'N/A')
            tags = ", ".join(match.get('tags', []))
            vulns = match.get('vulns', {})

            reply_lines.append(f"IP: {ip}")
            reply_lines.append(f"Org: {org}")
            reply_lines.append(f"ASN: {asn}")
            reply_lines.append(f"OS: {os_}")
            reply_lines.append(f"Location: {location}")
            reply_lines.append(f"Open ports: {ports}")
            if hostnames:
                reply_lines.append(f"Hostnames: {hostnames}")
            if tags:
                reply_lines.append(f"Tags: {tags}")
            if vulns:
                reply_lines.append(f"Vulnerabilities: {', '.join(vulns.keys())}")
            reply_lines.append(f"First seen: {timestamp}")

            banner_data = match.get('data', '').strip()
            if banner_data:
                banner_data = (banner_data[:700] + '...') if len(banner_data) > 700 else banner_data
                reply_lines.append(f"Banner:\n{banner_data}")
            reply_lines.append("-" * 40)

        reply_text = "\n".join(reply_lines)

        # Send the text reply first
        await update.message.reply_text(reply_text)

        # Generate markdown report and send as file
        md_report = create_markdown_report(domain, "Domain", reply_lines)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_md_file:
            tmp_md_file.write(md_report.encode('utf-8'))
            tmp_md_filepath = tmp_md_file.name

        with open(tmp_md_filepath, "rb") as doc_file:
            await update.message.reply_document(document=InputFile(doc_file, filename=f"shodan_report_{domain}.md"))

    except shodan.APIError as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        if tmp_md_filepath and os.path.exists(tmp_md_filepath):
            os.remove(tmp_md_filepath)

async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ip <ip_address>")
        return
    ip = context.args[0]
    tmp_md_filepath = None  # initialize for safety
    try:
        host = api.host(ip, history=True, minify=False)

        reply_lines = [
            f"IP: {ip}",
            f"Org: {host.get('org', 'N/A')}",
            f"ASN: {host.get('asn', 'N/A')}",
            f"OS: {host.get('os', 'N/A')}",
            f"Hostnames: {', '.join(host.get('hostnames', [])) or 'N/A'}",
            f"Location: {host.get('city', 'N/A')}, {host.get('country_name', 'N/A')}",
            f"Number of open ports: {len(host.get('ports', []))}",
            f"Open ports: {', '.join(str(port) for port in host.get('ports', []))}",
            f"Last update: {host.get('last_update', 'N/A')}",
        ]

        vulns = host.get('vulns', {})
        if vulns:
            reply_lines.append(f"Vulnerabilities: {', '.join(vulns.keys())}")

        reply_lines.append("\n=== Current Service Banners (up to 5) ===")
        for service in host.get('data', [])[:5]:
            reply_lines.append(format_service_banner(service))
            reply_lines.append("-" * 30)

        if 'history' in host and host['history']:
            reply_lines.append("\n=== Historical Service Banners (up to 3) ===")
            for i, hist in enumerate(host['history'][:3]):
                ts = hist.get('timestamp', 'N/A')
                reply_lines.append(f"\n--- History entry {i+1}: {ts} ---")
                for service in hist.get('data', [])[:3]:
                    reply_lines.append(format_service_banner(service))
                reply_lines.append("-" * 30)

        reply_text = "\n".join(reply_lines)

        # Send the text reply first
        await update.message.reply_text(reply_text)

        # Generate markdown report and send as file
        md_report = create_markdown_report(ip, "IP", reply_lines)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_md_file:
            tmp_md_file.write(md_report.encode('utf-8'))
            tmp_md_filepath = tmp_md_file.name

        with open(tmp_md_filepath, "rb") as doc_file:
            await update.message.reply_document(document=InputFile(doc_file, filename=f"shodan_report_{ip}.md"))

    except shodan.APIError as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        if tmp_md_filepath and os.path.exists(tmp_md_filepath):
            os.remove(tmp_md_filepath)

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("domain", domain_command))
    application.add_handler(CommandHandler("ip", ip_command))

    application.run_polling()

if __name__ == '__main__':
    main()

```
## How this works:

1. When a user runs /domain <domain> or /ip <ip>, the bot sends a text message with detailed Shodan data.
2. Immediately after, it generates a Markdown report file containing the same detailed info.
3. The bot sends the .md file as a document to the user for download.
4. Temporary files are cleaned up after sending.
5. The /start command sends your intro/instruction text.

## What you need to do:
1. Replace 'YOUR_SHODAN_API_KEY' and 'YOUR_TELEGRAM_BOT_TOKEN' with your actual keys.
2. Ensure you have python-telegram-bot v20+ and shodan installed:

```
pip install python-telegram-bot --upgrade
pip install shodan
```
Run the script locally.

