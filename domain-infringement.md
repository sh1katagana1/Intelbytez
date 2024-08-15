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
python83 opensquat.py -p month -k keywords.txt
```

