# Domain Infringement
In this lesson I want to go over some methods to monitor for Domain Infringement. Companies have identities, brands, domains, etc. that they need to protect as threat actors try to constantly impersonate them. There is some expensive commercial options, but there is also some low cost/free options you can use to do this task. I want to cover some tools and techniques I use to daily monitor if threat actors are attempting to impersonate the company I work for. 

## Open Squat
https://github.com/atenreiro/opensquat

***

The first and most important tool in my arsenal is Open Squat, it is the one that has produced the best results for me. Open Squat is a tool for identifying domain look-alikes by searching for newly registered domains that might be impersonating legit domains and brands. Threat actors like to register domain names that are very similar looking to their targets, typically called typosquatting. Sometimes they will add characters, substitute characters, swap letters for numbers, etc. \
**Install**
```
git clone https://github.com/atenreiro/opensquat
```
```
pip3 install -r requirements.txt
```
With a default installation, it will create a keywords.txt file that you are going to put target keywords into, as the tool does not take domain names, just keywords. Here is an example where I uncomment Google and add a keyword of pepsi:
```
#This is a comment
google
#facebook
#amazon
#paypal
#microsoft
pepsi
```
This is where you would add any keywords related to your company, domain, brand, etc. Open Squat will grab a list of the latest domains registered feed and try multiple permutations of the keywords in this file. It will then check these permutations against the list of domain names registered and if it sees a match it will list it with a confidence rating and you can investigate it further. \
**Basic Usage**
```
python3 opensquat.py -k keywords.txt
```
This will run Open Squat using the keywords file. Keep in mind this does not have to be the keywords.txt that comes with Open Squat, you can make your own, just pass in the correct name. When its finished running it will display a list of anything it finds. You can also go to the website https://opensquat.com/ to run a search on keywords, but it only uses the last 24 hours domain registered list. If you want to do a longer period of time, you have to use the command line tool.
```
python3 opensquat.py -p month -k keywords.txt
```
This has always given me great results that were quite accurate. 

## DNSTwist
https://github.com/elceef/dnstwist

***

This is my second go to tool. This one only takes domain names for input, and also does permutations of the supplied domain name. \
**Install**
```
pip3 install dnstwist[full]
```
**Basic Usage** \
This will run permutations of the domain name and check if any of these permutations are currently registered
```
dnstwist --registered domain.name
```
This will run permutations and check only for ones that are not currently registered. This is useful for your company to see what possible domains a threat actor may buy and buy them ahead of time instead, beating the threat actor to it. 
```
dnstwist -u domain.name
```
An additional thing the tool has is the ability to do fuzzy hashing to narrow down which domains you can priortize investigating. Fuzzy hashing is a concept that involves the ability to compare two inputs (HTML code) and determine a fundamental level of similarity, while perceptual hash is a fingerprint derived from visual features of an image (web page screenshot). The unique feature of detecting similar HTML source code can be enabled with --lsh argument. For each generated domain, dnstwist will fetch content from responding HTTP server (following possible redirects), normalize HTML code and compare its fuzzy hash with the one for the original (initial) domain. The level of similarity is expressed as a percentage. In cases when the effective URL is the same as for the original domain, the fuzzy hash is not calculated at all in order to reject false positive indications. 
```
dnstwist -r --lsh tlsh domain.name
```
The results will show a percentage and ones with a high percentage are definitely ones you should investigate further. It doesnt mean you dont investgate the other results, but sometimes the amount of results is quite large and you may want to prioritize what to investigate first. Like Open Squat, there is a web version you can use as well that defaults to results of registered domains https://dnstwist.it/

## Additional Links
[Have I Been Squatted](https://www.haveibeensquatted.com/) This site will have you put in a domain name and it will check if it has been squatted. It gives some additional info if you sign up such as whois data. The results look similar to DNSTwist and Open Squat as far as permutations go. It is unique in that it uses something called Levenshtein distance to determine how close it is to the given domain name (the smaller the distance, the higher the similarity). The Levenshtein distance is a number that tells you how different two strings are. The higher the number, the more different the two strings are. For example, the Levenshtein distance between “kitten” and “sitting” is 3 since, at a minimum, 3 edits are required to change one into the other. It looks like this site uses a Rust permutation generator https://github.com/haveibeensquatted/twistrs

