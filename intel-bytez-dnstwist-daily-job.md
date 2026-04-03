# DNSTwist Daily Run Job

***

## Goals
To have a daily cronjob task that runs dnstwist against a list of domains I am monitoring for infringement. I want to include the -whois switch to make sure I am reviewing the most recent registrations. The text output should sort the most recent date to the top of each domain list. 

## Setup
I have an Ubuntu Instance running in Oracle Cloud. I start with these commands:
```
mkdir ~/dnstwist && cd ~/dnstwist
python3 -m venv venv
source venv/bin/activate
pip3 install dnstwist[full]
```
This makes a directory called dnstwist, then creates a python virtual environment. I activate this environment and install the Python DNStwist library. This means the activation of the venv has to happen everytime the following script runs, even though its a BASH script. Inside the script we tell it to run the source venv/bin/activate each time it runs, so it should not be an issue. Create a text file list of domains you want to permutate and check called domains.txt in the same directory. Then create the following script:

## run_dnstwist.sh
```
#!/bin/bash

# 1. Configuration
BASE_DIR="/home/ubuntu/dnstwist"
INPUT_FILE="$BASE_DIR/domains.txt"
TIMESTAMP=$(date +"%Y-%m-%d")
FINAL_OUTPUT="$BASE_DIR/report_$TIMESTAMP.txt"

# 2. Preparation
cd $BASE_DIR
# Ensure we are in the virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found in $BASE_DIR/venv"
    exit 1
fi

echo "DNSTWIST Daily Infringement Report - $TIMESTAMP" > "$FINAL_OUTPUT"
echo "================================================" >> "$FINAL_OUTPUT"

# 3. Processing
while IFS= read -r domain || [ -n "$domain" ]; do
    # Clean up the input line (remove whitespace/empty lines)
    domain=$(echo "$domain" | tr -d '\r' | xargs)
    [ -z "$domain" ] && continue
    
    echo "Scanning $domain..."
    
    # Run dnstwist and output to CSV
    dnstwist --registered --whois --format csv "$domain" > temp.csv
    
    echo -e "\n[+] NEWEST REGISTERED RESULTS FOR: $domain" >> "$FINAL_OUTPUT"
    echo "------------------------------------------------" >> "$FINAL_OUTPUT"
    
    # The "Smart Sort" Logic:
    # - NF is the number of fields in the CSV line
    # - It looks for the column containing the YYYY-MM-DD date format
    # - It prepends the date to the line, sorts it, then removes the prepended date
    tail -n +2 temp.csv | awk -F, '{
        found=0;
        for(i=1;i<=NF;i++) {
            if($i ~ /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/) {
                print $i "|" $0; 
                found=1; 
                break;
            }
        }
        if(found==0) { print "0000-00-00|" $0; }
    }' | sort -r | cut -d'|' -f2- >> "$FINAL_OUTPUT"

done < "$INPUT_FILE"

# 4. Cleanup
if [ -f "temp.csv" ]; then rm temp.csv; fi
deactivate

echo "Scan complete. Report saved to: $FINAL_OUTPUT"
```
Make sure to give permissions to it:
```
chmod +x run_dnstwist.sh
```
The script takes in a list of domains called domains.txt. It does the default permutations and also uses the -whois switch to show when the domain was registered. This is so you can just monitor for ones that are newest, not old ones you already knew about. It outputs it to a text file and breaks it into sections per domain and scans the rows for the Date format and cycles the newest date to the top of each list. 

## Crontab
To set the job, run this:
```
crontab -e
```
Then at the bottom put this:
```
0 6 * * * /bin/bash /home/ubuntu/dnstwist/run_dnstwist.sh >> /home/ubuntu/dnstwist/cron_debug.log 2>&1
```
This will run every morning at 6AM and also output a log if something goes wrong.

