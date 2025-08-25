# Ascii QR Code test

***

## Goal
To create a proof of concept that creates an ASCII QR code to see if it bypasses email security tooling.

## Language 
Python for the QR code generation and HTML for the page that displays the QR code

## Script to generate QR code
```
import qrcode

qr = qrcode.QRCode(border=1)
qr.add_data('https://malicious-site.example/phish')
qr.make(fit=True)
matrix = qr.get_matrix()

# Render as ASCII - use '█' for black, ' ' for white
ascii_qr = ''
for row in matrix:
    ascii_qr += ''.join(['█' if cell else ' ' for cell in row]) + '\n'
print(ascii_qr)
```

## Breakdown
```
import qrcode
```
Imports the qrcode module. This Python library allows creating QR codes easily. To use it, it must first be installed (pip install qrcode). It provides high-level classes and functions for building and customizing QR codes

```
qr = qrcode.QRCode(border=1)
```
1. Creates a QRCode object. This object will manage the QR code’s properties and content.
2. border=1 sets the width of the white border space (measured in QR modules), which is the minimum allowed in the QR standard and produces a compact code

```
qr.add_data('https://malicious-site.example/phish')
```
1. Adds the data to be encoded in the QR code.
2. In this line, it uses a sample phishing URL—replace with any string or URL to encode.
3. The data is stored in the QR code’s matrix to be transformed into black and white squares.

```
qr.make(fit=True)
```
1. Builds (finalizes) the QR code matrix.
2. fit=True means the library automatically chooses the smallest version (size/dimension) of QR code that fits the provided data

```
matrix = qr.get_matrix()
```
1. Extracts the QR code as a matrix of booleans.
2. The .get_matrix() method returns a two-dimensional Python list (list of lists).
3. Each sublist represents a row; each element is a boolean (True = black “filled” square, False = white “blank” square). This provides direct access to the QR layout for custom rendering.

```
# Render as ASCII - use '█' for black, ' ' for white
ascii_qr = ''
for row in matrix:
    ascii_qr += ''.join(['█' if cell else ' ' for cell in row]) + '\n'
print(ascii_qr)
```
1. ascii_qr = '': Initializes an empty string to hold the ASCII QR art.
2. For every row in the matrix, it creates a string where each cell is either '█' (if black/filled/True) or ' ' (if white/blank/False), using a list comprehension and join.
3. Each finished row line is appended with \n for a line break.
4. After all rows, the QR code is represented as a grid of block characters, forming a readable ASCII QR code.
5. print(ascii_qr) displays the ASCII QR in the Python console or terminal—the result can be copied, pasted, or embedded into other contexts

Run the script and add a > to output it to a text file for easy copying.


## Script for the HTML
```
<html>
  <body>
    <p>To verify your account, scan the QR code below:</p>
    <pre style="font-size:16px; line-height:16px; letter-spacing:1px;">
█████████  █████████
█         █         █
█ ███████ █ ███████ █
█ █     █ █ █     █ █
█████████  █████████
    </pre>
    <p>
      <b>Note:</b> Scan using your phone camera to proceed.
    </p>
  </body>
</html>
```

Replace the ascii section above with your ascii that was generated. The ASCII QR code was put inside an HTML <pre> block to preserve the exact formatting, spacing, and line breaks of the ASCII characters as intended by the creator. This is crucial for ASCII art or text-based QR codes because their visual appearance and alignment depend on fixed-width spacing and exact line breaks.

Key reasons for using <pre>:
1. Preserves whitespace: Unlike normal HTML, which collapses multiple spaces and ignores line breaks, the <pre> tag ensures all spaces and newlines are rendered exactly as written, maintaining the QR code’s grid structure.
2. Uses monospace font by default: The <pre> element displays text in a fixed-width (monospace) font, where every character occupies the same horizontal space. This consistency is essential to keep the QR code’s pixel-like blocks aligned properly across rows and columns.
3. Prevents visual distortion: Without <pre>, browsers merge consecutive spaces and line breaks, causing the ASCII QR code to lose its block shape and become unreadable by scanning apps.
4. Simple and reliable: The <pre> tag is the simplest and most semantically correct way in HTML to display preformatted text such as code snippets, logs, or ASCII art, guaranteeing consistent display across browsers and email clients.



































