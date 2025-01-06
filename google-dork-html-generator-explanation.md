Google Dork HTML generator Script Explanation

## Goal
Create a script that takes in a text file list of google dorks on separate lines called dorks.txt, an example being: filetype:pdf AND "confidential". Have it also take in a domain name as an input. Have the script use this input as a value for site: google dork and populate every google dork in the dorks.txt file with this site: and the domain name from the input. Have the script generate an HTML page where each newly created dork is listed with a button beside them for the user to click and have it open in a new window with this populated google dork

## Script
```
import sys
from urllib.parse import quote_plus

def generate_html(dorks, domain):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Dorks for {domain}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .dork {{ margin-bottom: 10px; }}
            .dork-text {{ display: inline-block; width: 80%; }}
            .search-btn {{ padding: 5px 10px; }}
        </style>
    </head>
    <body>
        <h1>Google Dorks for {domain}</h1>
        {dork_list}
    </body>
    </html>
    """

    dork_items = []
    for dork in dorks:
        full_dork = f'site:{domain} {dork}'
        encoded_dork = quote_plus(full_dork)
        dork_items.append(f"""
        <div class="dork">
            <span class="dork-text">{full_dork}</span>
            <button class="search-btn" onclick="window.open('https://www.google.com/search?q={encoded_dork}', '_blank')">Search</button>
        </div>
        """)

    return html.format(domain=domain, dork_list='\n'.join(dork_items))

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <dorks_file> <domain>")
        sys.exit(1)

    dorks_file = sys.argv[1]
    domain = sys.argv[2]

    try:
        with open(dorks_file, 'r') as file:
            dorks = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{dorks_file}' not found.")
        sys.exit(1)

    html_content = generate_html(dorks, domain)

    output_file = f"google_dorks_{domain}.html"
    with open(output_file, 'w') as file:
        file.write(html_content)

    print(f"HTML file '{output_file}' has been generated successfully.")

if __name__ == "__main__":
    main()
```

## What does this script do?
This script does the following:

1. It takes two command-line arguments: the path to the dorks.txt file and the domain name.
2. It reads the dorks from the file, stripping any whitespace and ignoring empty lines.
3. It generates an HTML page with each dork listed along with a "Search" button.
4. Each button, when clicked, opens a new window with a Google search for the dork, including the site: operator with the specified domain.
5. The generated HTML file is saved as google_dorks_<domain>.html in the same directory as the script.

## Usage
To use the script, save it as google_dorks_generator.py and run it from the command line like this:

```
python google_dorks_generator.py dorks.txt example.com
```
This will generate an HTML file named google_dorks_example.com.html with all the dorks and search buttons


## Modification Goals
Modify the script so that I can modify my dorks.txt list to include a description text, for example: filetype:pdf AND "confidential" ***PDF file search. Have the script parse the words after *** on each line and put those words in the button instead of the word Search

## Script
```
import sys
from urllib.parse import quote_plus

def parse_dork_line(line):
    parts = line.split('***')
    dork = parts[0].strip()
    description = parts[1].strip() if len(parts) > 1 else "Search"
    return dork, description

def generate_html(dorks, domain):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Dorks for {domain}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .dork {{ margin-bottom: 10px; }}
            .dork-text {{ display: inline-block; width: 80%; }}
            .search-btn {{ padding: 5px 10px; }}
        </style>
    </head>
    <body>
        <h1>Google Dorks for {domain}</h1>
        {dork_list}
    </body>
    </html>
    """

    dork_items = []
    for dork, description in dorks:
        full_dork = f'site:{domain} {dork}'
        encoded_dork = quote_plus(full_dork)
        dork_items.append(f"""
        <div class="dork">
            <span class="dork-text">{full_dork}</span>
            <button class="search-btn" onclick="window.open('https://www.google.com/search?q={encoded_dork}', '_blank')">{description}</button>
        </div>
        """)

    return html.format(domain=domain, dork_list='\n'.join(dork_items))

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <dorks_file> <domain>")
        sys.exit(1)

    dorks_file = sys.argv[1]
    domain = sys.argv[2]

    try:
        with open(dorks_file, 'r') as file:
            dorks = [parse_dork_line(line) for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{dorks_file}' not found.")
        sys.exit(1)

    html_content = generate_html(dorks, domain)

    output_file = f"google_dorks_{domain}.html"
    with open(output_file, 'w') as file:
        file.write(html_content)

    print(f"HTML file '{output_file}' has been generated successfully.")

if __name__ == "__main__":
    main()
```

## What does this modified script do?
This modified script now:

1. Parses each line in the dorks.txt file, splitting it into the dork and description parts using the '***' separator
2. Uses the description text (if provided) as the button text instead of "Search"
3. If no description is provided after '***', it defaults to "Search" for the button text.

## Usage
To use this script, your dorks.txt file should now look like this:

```
filetype:pdf AND "confidential" ***PDF file search
inurl:admin ***Admin page search
```
Run the script the same way as before:

```
python google_dorks_generator.py dorks.txt example.com
```
This will generate an HTML file with the dorks and custom button texts based on the descriptions provided in the dorks.txt file