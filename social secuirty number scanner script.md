# Search SSN in documents

***


## Goal
To create a Python script that searches a text file for social security numbers in the format xxx-xx-xxxx, you can use regular expressions.

## Script
```
import re

def find_social_security_numbers(file_path):
    """
    Searches a text file for social security numbers in the format xxx-xx-xxxx.

    Args:
        file_path (str): The path to the text file to search.

    Returns:
        list: A list of found social security numbers.
    """
    # Regular expression pattern for social security numbers
    pattern = r'\b\d{3}-\d{2}-\d{4}\b'

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Find all matches of the pattern in the file content
            social_security_numbers = re.findall(pattern, content)
            return social_security_numbers
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

if __name__ == "__main__":
    file_path = input("Enter the path to the text file: ")
    social_security_numbers = find_social_security_numbers(file_path)

    if social_security_numbers:
        print("Found Social Security Numbers:")
        for ssn in social_security_numbers:
            print(ssn)
    else:
        print("No social security numbers found in the file.")
```

## How to Use the Script
1. Save the Script: Save the above code in a file, for example, find_ssn.py.
2. Run the Script: Execute the script using Python:
```
python find_ssn.py
```
3. Input File Path: When prompted, enter the path to the text file you want to search.

## Explanation

1. Regular Expression: The regular expression \b\d{3}-\d{2}-\d{4}\b matches strings that are exactly in the format xxx-xx-xxxx, where x is a digit.
2. File Reading: The script reads the entire content of the specified file.
3. Finding Matches: The re.findall function is used to find all occurrences of the pattern in the file content.
4. Error Handling: The script handles the case where the specified file does not exist.

This script will print out all social security numbers found in the specified text file.
--------------------------------


## Modification Goal
To handle cases where the social security number (SSN) format is not exactly xxx-xx-xxxx, you can implement several strategies for validation, formatting, and error handling. 

## Validation Using Regular Expressions
You can use regular expressions to validate if the input matches the xxx-xx-xxxx format. Here is an example in Python:

## Script

```
import re

def validate_ssn(ssn):
    pattern = r'^\d{3}-\d{2}-\d{4}$'
    if re.match(pattern, ssn):
        return True
    else:
        return False

# Example usage
ssn = input("Enter the Social Security Number: ")
if validate_ssn(ssn):
    print("Valid SSN format")
else:
    print("Invalid SSN format. Please use xxx-xx-xxxx.")
```

***


## Handling Different Formats
If the input might be in different formats (e.g., without dashes or with extra characters), you can preprocess the input to standardize it before validation.
```
import re

def standardize_ssn(ssn):
    # Remove all non-digit characters
    ssn = re.sub(r'\D', '', ssn)
    # Check if the length is correct
    if len(ssn)!= 9:
        return None
    # Format the SSN
    return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"

def validate_ssn(ssn):
    standardized_ssn = standardize_ssn(ssn)
    if standardized_ssn:
        return standardized_ssn
    else:
        return None

# Example usage
ssn = input("Enter the Social Security Number: ")
validated_ssn = validate_ssn(ssn)
if validated_ssn:
    print(f"Valid SSN format: {validated_ssn}")
else:
    print("Invalid SSN format. Please use xxx-xx-xxxx or a similar format.")
```

***


## Error Handling With Informative Error Messages
Provide clear and informative error messages to help users correct their input.
```
def validate_ssn(ssn):
    pattern = r'^\d{3}-\d{2}-\d{4}$'
    if re.match(pattern, ssn):
        return True
    else:
        print("Invalid SSN format. Please use xxx-xx-xxxx.")
        return False

# Example usage
ssn = input("Enter the Social Security Number: ")
if not validate_ssn(ssn):
    while not validate_ssn(ssn):
        ssn = input("Enter the Social Security Number again: ")
```

***


## Client-Side and Server-Side Validation With HTML and JavaScript Validation
For web applications, you can use HTML5 pattern attribute along with JavaScript to validate the SSN format on the client side. However, always validate on the server side as well to prevent bypassing client-side validation2.

xml
```
<label>
    Social Security Number:
    <input id="ssn" required pattern="^\d{3}-\d{2}-\d{4}$" title="Expected pattern is ###-##-####" />
</label>

<script>
    document.getElementById('ssn').addEventListener('input', function() {
        if (!this.value.match(/^\d{3}-\d{2}-\d{4}$/)) {
            this.setCustomValidity('Invalid SSN format. Please use xxx-xx-xxxx.');
        } else {
            this.setCustomValidity('');
        }
    });
</script>
```

***


## Server-Side Validation
Ensure that server-side validation is implemented to handle cases where client-side validation might be bypassed.

```
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/validate_ssn', methods=['POST'])
def validate_ssn():
    ssn = request.json.get('ssn')
    pattern = r'^\d{3}-\d{2}-\d{4}$'
    if re.match(pattern, ssn):
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False, 'error': 'Invalid SSN format. Please use xxx-xx-xxxx.'})

if __name__ == '__main__':
    app.run()
```
By combining these strategies, you can effectively handle and validate SSNs in various formats, ensuring that the input is correct and consistent.