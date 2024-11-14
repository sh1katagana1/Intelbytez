# Domain Expiry Check

***


## Goal
To create a script that takes in a list of domains from a text file and looks for their expiration dates and displays the results on screen.

```
## Script (.sh)
#!/bin/bash

# Check if whois is installed
if ! command -v whois &> /dev/null; then
    echo "Error: whois command not found. Please install whois."
    exit 1
fi

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <domain_list_file>"
    exit 1
fi

# Read the domain list file
domain_file="$1"

if [ ! -f "$domain_file" ]; then
    echo "Error: File '$domain_file' not found."
    exit 1
fi

# Function to get expiration date
get_expiration_date() {
    local domain="$1"
    whois "$domain" | grep -i "expir" | grep -i "date" | awk '{print $NF}' | head -n 1
}

# Print header
printf "%-30s %-30s %-15s\n" "Domain" "Expiration Date" "Days Left"
echo "----------------------------------------------------------------------"

# Process each domain
while IFS= read -r domain || [[ -n "$domain" ]]; do
    expiration_date=$(get_expiration_date "$domain")
    
    if [ -z "$expiration_date" ]; then
        printf "%-30s %-30s %-15s\n" "$domain" "Unable to retrieve" "N/A"
    else
        # Calculate days left
        current_date=$(date +%s)
        expiration_timestamp=$(date -d "$expiration_date" +%s)
        days_left=$(( (expiration_timestamp - current_date) / 86400 ))
        
        printf "%-30s %-30s %-15s\n" "$domain" "$expiration_date" "$days_left days"
    fi
done < "$domain_file"
```

## What does the script do?

1. It checks if the whois command is installed.
2. It verifies that a file containing the list of domains is provided as an argument.
3. It defines a function get_expiration_date to extract the expiration date from the whois output.
4. It prints a header for the output.
5. It reads each domain from the provided file and processes it:
6. It retrieves the expiration date using the whois command.
7. If the expiration date is found, it calculates the number of days left until expiration.
8. It prints the domain, expiration date, and days left in a formatted table.



## Usage

1. Save it to a file, e.g., check_domain_expiry.sh.
2. Make it executable: chmod +x check_domain_expiry.sh.
3. Create a text file with one domain per line, e.g., domains.txt.
4. Run the script: ./check_domain_expiry.sh domains.txt.

The script will display a table with the domain names, their expiration dates, and the number of days left until expiration. Note that the accuracy of the results depends on the format of the whois output, which can vary between different domain registrars. You may need to adjust the get_expiration_date function if you encounter domains with differently formatted whois outputs.



## Modification
Modify the script to add a 5 second delay so as to not come against rate limiting.

## Script
```
#!/bin/bash

# Check if whois is installed
if ! command -v whois &> /dev/null; then
    echo "Error: whois command not found. Please install whois."
    exit 1
fi

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <domain_list_file>"
    exit 1
fi

# Read the domain list file
domain_file="$1"

if [ ! -f "$domain_file" ]; then
    echo "Error: File '$domain_file' not found."
    exit 1
fi

# Function to get expiration date
get_expiration_date() {
    local domain="$1"
    whois "$domain" | grep -i "expir" | grep -i "date" | awk '{print $NF}' | head -n 1
}

# Print header
printf "%-30s %-30s %-15s\n" "Domain" "Expiration Date" "Days Left"
echo "----------------------------------------------------------------------"

# Process each domain
while IFS= read -r domain || [[ -n "$domain" ]]; do
    expiration_date=$(get_expiration_date "$domain")
    
    if [ -z "$expiration_date" ]; then
        printf "%-30s %-30s %-15s\n" "$domain" "Unable to retrieve" "N/A"
    else
        # Calculate days left
        current_date=$(date +%s)
        expiration_timestamp=$(date -d "$expiration_date" +%s)
        days_left=$(( (expiration_timestamp - current_date) / 86400 ))
        
        printf "%-30s %-30s %-15s\n" "$domain" "$expiration_date" "$days_left days"
    fi

    # Add a delay between requests (adjust as needed)
    sleep 2
done < "$domain_file"
```

The main change in this script is the addition of a sleep 2 command at the end of the loop. This introduces a 2-second delay between each WHOIS request, which should help avoid rate limiting or denial of service from WHOIS servers. You can adjust the delay by changing the number after sleep. For example, sleep 5 would introduce a 5-second delay, which might be necessary if you're still encountering issues with a 2-second delay. Remember that different WHOIS servers may have different rate limiting policies, so you might need to experiment with the delay duration to find the right balance between speed and avoiding denial of service.





