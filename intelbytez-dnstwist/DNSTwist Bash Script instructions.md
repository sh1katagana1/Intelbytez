# DNSTwist Bash Script

***

## Goal
To utilize DNSTwist to take in a text file list of domains called domains.txt and permutate them using their algorithms. Additionally, use whois to determine the creation date and export to CSV so that you can filter for most recent registrations. Only search for registered domains.

## Process
Create a folder for this and install a python virtual environment
```
Python3 -m venv venv
```
Activate it
```
source venv/bin/activate
```
Install dnstwist
```
pip3 install dnstwist
```
Each time you running the following script, you need to come to this folder and activate the virtual environment before you run the script. save the following script as twist.sh, then give it permissions
```
chmod a+x twist.sh
```
Run the script
```
./twist.sh
```
This will give you a CSV file named permutations_final.csv

## Script
```
#!/bin/bash

# --- Configuration ---
INPUT_FILE="domains.txt"
OUTPUT_FILE="permutations_final.csv"

# List of common TLDs to use for swapping
TLD_FILE="common_tlds.txt"

# Create the TLD file if it doesn't exist
cat <<EOF > "$TLD_FILE"
com
net
org
info
biz
xyz
co
io
app
ai
tech
online
store
dev
us
EOF

# --- Execution ---
echo "✨ Starting bulk DNSTwist analysis from: $INPUT_FILE"
echo "Output will be saved to: $OUTPUT_FILE"
echo "--------------------------------------------------"

# Clear the output file
> "$OUTPUT_FILE"

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "🚨 Error: Input file '$INPUT_FILE' not found!"
    exit 1
fi

# Loop through each domain in the input file
while IFS= read -r domain
do
    # Skip empty lines or lines starting with '#'
    if [[ -z "$domain" || "$domain" =~ ^# ]]; then
        continue
    fi
    
    echo "Processing: $domain"
    
    # 1. Define a temporary file for the current domain's CSV output
    temp_csv="temp_${domain//./_}.csv"

    # 2. Run dnstwist with all required options
    # --tld $TLD_FILE: Generates permutations by swapping TLDs.
    # --whois: Adds the WHOIS creation date and registrar.
    # --registered: Shows only domains that are currently registered.
    # --format csv: Formats the entire output as CSV.
    dnstwist "$domain" \
        --tld "$TLD_FILE" \
        --whois \
        --registered \
        --format csv > "$temp_csv"

    # 3. Combine the temporary CSV into the final output file
    if [ ! -s "$OUTPUT_FILE" ]; then
        # If the final output is empty, copy the header and data from the temp file
        cat "$temp_csv" > "$OUTPUT_FILE"
    else
        # If the final output exists, skip the header row (first line) and append the data
        tail -n +2 "$temp_csv" >> "$OUTPUT_FILE"
    fi

    # 4. Clean up the temporary file
    rm "$temp_csv"
    
done < "$INPUT_FILE"

# Clean up the TLD file (optional)
rm "$TLD_FILE"

echo "--------------------------------------------------"
echo "✅ Complete! All WHOIS-enriched permutations saved to $OUTPUT_FILE"
```

## Script Explanation
```
#!/bin/bash
```
1. This tells your computer which program should run the script
2. /bin/bash is the Bash shell (a command-line language)
3. When you run this file, the system knows to execute it using Bash

Think of it like saying: "Hey computer, run this file using Bash."

```
# --- Configuration ---
INPUT_FILE="domains.txt"
OUTPUT_FILE="permutations_final.csv"
```
1. You’re creating variables, which are named containers for values
2. INPUT_FILE stores the name of the file that contains domains
3. OUTPUT_FILE stores the name of the final CSV file

This is useful if you ever want to change file names, you only change them once here. The rest of the script automatically uses the new names

```
# List of common TLDs to use for swapping
TLD_FILE="common_tlds.txt"
```
1. Another variable. This will hold a list of Top-Level Domains (.com, .net, .io, etc.)
2. DNSTwist will use these to generate domain variations, because the default is just .com. It can also be achieved by adding in a dictionary file and using the --tld switch. 

```
cat <<EOF > "$TLD_FILE"
com
net
org
info
biz
xyz
co
io
app
ai
tech
online
store
dev
us
EOF
```
1. cat <<EOF starts a multi-line input
2. Everything until EOF is written into a file
3. > "$TLD_FILE" sends that content into common_tlds.txt
4. A file called common_tlds.txt is created
5. Each line contains one TLD

Think of it as: "Create a text file and paste these TLDs into it automatically."

```
echo " Starting bulk DNSTwist analysis from: $INPUT_FILE"
echo "Output will be saved to: $OUTPUT_FILE"
echo "--------------------------------------------------"
```
1. echo prints text to the terminal
2. $INPUT_FILE and $OUTPUT_FILE get replaced with their values
3. This helps the user see what’s happening

```
> "$OUTPUT_FILE"
```
1. Creates the output file if it doesn’t exist
2. Empties it if it does exist so you don’t accidentally append new results to old data

```
if [ ! -f "$INPUT_FILE" ]; then
    echo " Error: Input file '$INPUT_FILE' not found!"
    exit 1
fi
```
1. if starts a condition
2. -f "$INPUT_FILE" checks if a file exists
3. ! means "not"
4. So this means: "If the input file does NOT exist…" Then print an error message
5. exit 1 stops the script immediately (with an error code) This prevents the script from crashing later.

```
while IFS= read -r domain
do
```
1. This is a loop.
2. Reads domains.txt one line at a time
3. Each line gets stored in the variable domain
4. The loop runs once per domain
5. As long as something succeeds, keep running the commands.
6. IFS stands for Internal Field Separator. By default, Bash splits input on Spaces, Tabs and Newlines. If I do IFS= with a space, as is here, it means do NOT split the line on spaces. This means the entire line is read exactly as-is. 
7. The -r option means read the line raw. For example, normally if you use \ that is an escape character. Reading it raw means its just seen as \ not as an escape character. 

Think of it like: "For each domain in the file, do the following…"


```
if [[ -z "$domain" || "$domain" =~ ^# ]]; then
    continue
fi
```
1. This is a filter.
2. It skips empty lines (-z means "zero length") and lines starting with # (comments)
3. continue means: "Skip this line and move to the next one." This keeps your input file clean and flexible.

```
echo "Processing: $domain"
```
Just a progress message so you know which domain is currently being processed

```
temp_csv="temp_${domain//./_}.csv"
```
1. Creates a temporary filename based on the domain name. If the domain name is example.com, then we want temp_example_com.csv to be generated.
2. Replaces dots (.) in the domain with underscores (_)
3. Example: example.com -> temp_example_com.csv
4. temp_csv="..." means store this text in a variable called temp_csv.
5. ${domain//./_} This is called parameter expansion in Bash. It means "Take the value of domain and transform it". As an example, if you have this: ${variable//pattern/replacement} your saying replace every occurrence of pattern with replacement. So when we do ${domain//./_} this replaces every dot with an underscore.

This is because dots can cause issues in filenames. Each domain gets its own temporary CSV.


```
dnstwist "$domain" \
    --tld "$TLD_FILE" \
    --whois \
    --registered \
    --format csv > "$temp_csv"
```
1. This is where we run Dnstwist
2. The options are as follows:
* "$domain" → domain to analyze
* --tld "$TLD_FILE" → swap TLDs using your list
* --whois → add WHOIS data
* --registered → only show registered domains
* --format csv → output as CSV
* > "$temp_csv" → save output to a file

Generate domain permutations for this domain and save them as CSV

```
if [ ! -s "$OUTPUT_FILE" ]; then
    cat "$temp_csv" > "$OUTPUT_FILE"
else
    tail -n +2 "$temp_csv" >> "$OUTPUT_FILE"
fi
```
1. This avoids duplicate CSV headers.
2. -s checks if the file has content
3. If the output file is empty: Copy everything (including headers)
4. If it already has data: Skip the first line (tail -n +2)
5. Append only the data

This is a very common CSV-handling trick

Each time you run dnstwist, it creates a CSV file like this:
```
domain,domain_ascii,registrar,creation_date,...
example1.com,...
example2.com,...
```
Because the first row is a header, every temporary CSV has the same header. If you simply appended every temp file: 
```
cat temp_*.csv >> permutations_final.csv
```
You’d end up with:
```
domain,domain_ascii,registrar,...
example1.com,...
domain,domain_ascii,registrar,...
example2.com,...
```
This will break CSV parsing. You want keep the header once and append only data rows afterward. the first section is checking if output_file is empty or not. The cat command copies everything from the temp CSV including the header row and writes it into the output file. 

Second case: output file already has data. 
```
tail -n +2 "$temp_csv" >> "$OUTPUT_FILE"
```
This means print the file starting from line 2 onward, which skips line 1, which is the header. This keeps only the data rows and adds the data to the end of the output file. It does NOT overwrite existing content. 


```
rm "$temp_csv"

```
Deletes the temporary CSV to keep things tidy.


```
done < "$INPUT_FILE"
```
This tells Bash: "Keep looping until all lines in domains.txt are read."


```
rm "$TLD_FILE"
```
Deletes the temporary TLD list and keeps your directory clean. Optional, but nice


```
echo "--------------------------------------------------"
echo "✅ Complete! All WHOIS-enriched permutations saved to $OUTPUT_FILE"
```
Confirms that the script finished successfully and the final CSV is ready.

















