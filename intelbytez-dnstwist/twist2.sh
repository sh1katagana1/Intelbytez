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
