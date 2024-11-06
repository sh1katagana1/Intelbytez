# APK Store Google Dork Search Tool For Rogue Mobile Apps

***

## Goal
To create an html file that will search the google dork of site:apkpure.com and the keyword is submitted via a text field and button

## Script (HTML)
```
!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APKPure Google Dork Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        #searchForm {
            margin-top: 20px;
        }
        #keyword {
            width: 70%;
            padding: 10px;
            font-size: 16px;
        }
        #searchButton {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        #searchButton:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>APKPure Google Dork Search</h1>
    <form id="searchForm">
        <input type="text" id="keyword" placeholder="Enter your search keyword" required>
        <button type="submit" id="searchButton">Search</button>
    </form>

    <script>
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            var keyword = document.getElementById('keyword').value;
            var searchUrl = 'https://www.google.com/search?q=site:apkpure.com+' + encodeURIComponent(keyword);
            window.open(searchUrl, '_blank');
        });
    </script>
</body>
</html>
```

## What does this script do?
This HTML file creates a simple web page with the following features:

1. A title "APKPure Google Dork Search"
2. A text input field for the user to enter their search keyword
3. A "Search" button to submit the query
4. Basic styling to make the page look presentable
5. JavaScript code that handles the form submission

When the user enters a keyword and clicks the "Search" button, the script constructs a Google search URL with the site:apkpure.com dork and the user's keyword. It then opens this URL in a new tab or window, displaying the Google search results for the specified dork and keyword.

## Usage
To use this HTML file:

1. Copy the entire code above and save it as a .html file (e.g., "apkpure_dork_search.html")
2. Open the file in a web browser
3. Enter a keyword in the text field and click "Search"
4. A new tab or window will open with the Google search results for the specified dork and keyword

## Modification Goal
Modify the HTML file to include additional sites in the Google dork search. Here's the updated version that includes site:apkpure.com, site:apkmonk.com, site:apkmirror.com, site:apkcombo.com, site:aptoide.com, site:apkbe.com, and site:apk4fun.com:

## Script (HTML)
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APK Google Dork Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        #searchForm {
            margin-top: 20px;
        }
        #keyword {
            width: 70%;
            padding: 10px;
            font-size: 16px;
        }
        #searchButton {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        #searchButton:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <h1>APK Google Dork Search</h1>
    <form id="searchForm">
        <input type="text" id="keyword" placeholder="Enter your search keyword" required>
        <button type="submit" id="searchButton">Search</button>
    </form>

    <script>
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            var keyword = document.getElementById('keyword').value;
            var sites = [
                'site:apkpure.com',
                'site:apkmonk.com',
                'site:apkmirror.com',
                'site:apkcombo.com',
                'site:aptoide.com',
                'site:apkbe.com',
                'site:apk4fun.com'
            ];
            var searchQuery = sites.join(' OR ') + ' ' + encodeURIComponent(keyword);
            var searchUrl = 'https://www.google.com/search?q=' + searchQuery;
            window.open(searchUrl, '_blank');
        });
    </script>
</body>
</html>
```
## What does this script do?
This updated version includes the following changes:

1. The title has been changed to "APK Google Dork Search" to reflect the broader scope of the search.
2. In the JavaScript code, we've created an array called sites that contains all the site-specific dorks.
3. We use the join(' OR ') method to combine all the site dorks with the OR operator, ensuring that Google searches across all specified sites.
4. The final search query is constructed by combining the site dorks with the user's keyword.

Now, when a user enters a keyword and clicks the "Search" button, the script will open a new tab with a Google search that includes all the specified sites. This allows users to search for APKs across multiple popular APK hosting websites simultaneously. 

## Usage
To use this HTML file:

1. Copy the entire code above and save it as a .html file (e.g., "apk_dork_search.html")
2. Open the file in a web browser
3. Enter a keyword in the text field and click "Search"
4. A new tab or window will open with the Google search results for the specified dorks and keyword across all the listed APK sites

