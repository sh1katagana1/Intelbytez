# Domain To Live Site Checker v2

***

## Goal
To create a bash script that takes in a list of domains from a text file, attempts to connect to them, follows all redirects and outputs the final url and http response code.

## Script (Bash)
```
#!/bin/bash

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Please provide a file containing domain names as an argument."
    exit 1
fi

# Read domains from the file
input_file="$1"

# Function to follow redirects and get final URL and status code
check_domain() {
    local domain="$1"
    local url="http://$domain"
    
    # Use curl to follow redirects and get final URL and status code
    result=$(curl -sS -o /dev/null -w "%{url_effective} %{http_code}" -L "$url")
    
    # Extract final URL and status code
    final_url=$(echo "$result" | cut -d' ' -f1)
    status_code=$(echo "$result" | cut -d' ' -f2)
    
    echo "$domain,$final_url,$status_code"
}

# Process each domain in the file
while IFS= read -r domain || [[ -n "$domain" ]]; do
    check_domain "$domain"
done < "$input_file"
```

## What does this script do?

1. It checks if a file is provided as an argument when running the script.
2. It defines a function called check_domain that takes a domain as input, attempts to connect to it using curl, follows all redirects, and returns the final URL and HTTP response code.
3. It reads domains from the input file line by line.
4. For each domain, it calls the check_domain function and outputs the results in the format: original domain, final URL, and HTTP status code.

## Usage

1. Save it to a file, for example, check_domains.sh.
2. Make it executable with chmod +x check_domains.sh.
3. Create a text file (e.g., domains.txt) containing one domain per line.
4. Run the script with the input file as an argument:

```
./check_domains.sh domains.txt
```
The script will output the results for each domain in the format:

```
original_domain,final_url,http_status_code
```
For example:

```
example.com,http://www.example.com,200
google.com,https://www.google.com/,200
```
This script uses curl to handle the HTTP requests and follow redirects. It captures the final URL and HTTP status code for each domain

## Modification 1
Modify the script to omit all domains that it cannot connect to

## Script
```
#!/bin/bash

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Please provide a file containing domain names as an argument."
    exit 1
fi

# Read domains from the file
input_file="$1"

# Function to follow redirects and get final URL and status code
check_domain() {
    local domain="$1"
    local url="http://$domain"
    
    # Use curl to follow redirects and get final URL and status code
    result=$(curl -sS -o /dev/null -w "%{url_effective} %{http_code}" -L --connect-timeout 10 "$url" 2>/dev/null)
    
    # Check if curl was successful
    if [ $? -eq 0 ]; then
        # Extract final URL and status code
        final_url=$(echo "$result" | cut -d' ' -f1)
        status_code=$(echo "$result" | cut -d' ' -f2)
        
        echo "$domain,$final_url,$status_code"
    fi
}

# Process each domain in the file
while IFS= read -r domain || [[ -n "$domain" ]]; do
    check_domain "$domain"
done < "$input_file"
```

## Here are the key changes made to the script:

1. In the check_domain function, we added a --connect-timeout 10 option to curl. This sets a 10-second timeout for the connection attempt.
2. We added 2>/dev/null to the curl command to suppress error messages.
3. After the curl command, we check its exit status using if [ $? -eq 0 ]. This condition will be true only if curl was successful in connecting to the domain.
4. We only output the domain information if the connection was successful. If curl fails to connect (due to an invalid domain, network issues, etc.), the script will silently skip that domain and move on to the next one.

## This modified script will:

1. Attempt to connect to each domain in the input file
2. Follow all redirects for successful connections
3. Output the original domain, final URL, and HTTP response code only for domains it can successfully connect to
4. Silently skip any domains it cannot connect to (due to invalid domains, network issues, etc.)

## Usage

1. Save it to a file, for example, check_domains.sh.
2. Make it executable with chmod +x check_domains.sh.
3. Create a text file (e.g., domains.txt) containing one domain per line.
4. Run the script with the input file as an argument:

```
./check_domains.sh domains.txt
```
The script will output results only for domains it can successfully connect to, in the format:

```
original_domain,final_url,http_status_code
```
This approach ensures that your output only includes valid, accessible domains


## Modification 2
Modify the script to ignore SSL errors

## Script
```
#!/bin/bash

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Please provide a file containing domain names as an argument."
    exit 1
fi

# Read domains from the file
input_file="$1"

# Function to follow redirects and get final URL and status code
check_domain() {
    local domain="$1"
    local url="https://$domain"
    
    # Use curl to follow redirects, ignore SSL errors, and get final URL and status code
    result=$(curl -sS -o /dev/null -w "%{url_effective} %{http_code}" -L --connect-timeout 10 -k "$url" 2>/dev/null)
    
    # Check if curl was successful
    if [ $? -eq 0 ]; then
        # Extract final URL and status code
        final_url=$(echo "$result" | cut -d' ' -f1)
        status_code=$(echo "$result" | cut -d' ' -f2)
        
        echo "$domain,$final_url,$status_code"
    fi
}

# Process each domain in the file
while IFS= read -r domain || [[ -n "$domain" ]]; do
    check_domain "$domain"
done < "$input_file"
```

## Here are the key changes made to the script to ignore SSL errors:

1. In the check_domain function, we changed the initial url to use https:// instead of http://. This ensures we're testing SSL connections.
2. We added the -k option to the curl command. This option tells curl to ignore SSL certificate errors. It's equivalent to using --insecure
3. We kept the --connect-timeout 10 option to maintain a 10-second timeout for the connection attempt.
4. We still use 2>/dev/null to suppress error messages, including any SSL-related warnings.

## This modified script will:

1. Attempt to connect to each domain in the input file using HTTPS
2. Ignore SSL certificate errors (such as self-signed certificates, expired certificates, etc.)
3. Follow all redirects for successful connections
4. Output the original domain, final URL, and HTTP response code only for domains it can successfully connect to
5. Silently skip any domains it cannot connect to (due to invalid domains, network issues, etc.)

## Usage

1. Save it to a file, for example, check_domains.sh.
2. Make it executable with chmod +x check_domains.sh.
3. Create a text file (e.g., domains.txt) containing one domain per line.
4. Run the script with the input file as an argument:

```
./check_domains.sh domains.txt
```
The script will output results for domains it can successfully connect to, ignoring SSL errors, in the format:

```
original_domain,final_url,http_status_code
```
Please note that while this script ignores SSL errors for testing purposes, it's important to be cautious when using this approach in production environments, as it bypasses security measures designed to protect against man-in-the-middle attacks and other SSL-related vulnerabilities.
.
