# Intel Bytez - Telegram RSS Feed Bot Instructions

***

## Goal
When performing cyber threat intel duties, a big part of your job is reviewing security blogs for the latest threat intel and cybersecurity news. You could bookmark all of these sites in your browser and visit them daily, or utilize Telegram. Telegram is a messaging app that I like to repurpose for mostly Threat Intel and OSINT tasks and they have a feature called 'bots'. These allow you to automate things and control and view them via Telegram. Our goal here is to create a Telegram bot that lets you type in the word /fetch and get the last 10 articles from a number of RSS feeds of cybersecurity sites.

## Blogs
There is a plethora of cybersecurity blogs, some with very focused purposes. Here is a list of some that I like to use: \
[GB Hackers](https://gbhackers.com/feed/) \
[Bleeping Computer](https://www.bleepingcomputer.com/feed/) \
[Cybersecurity News](https://cybersecuritynews.com/feed/) \
[Krebs On Security](https://krebsonsecurity.com/feed/) \
[SANS Internet Storm Center](https://isc.sans.edu/rssfeed_full.xml) \
[Schneier](https://www.schneier.com/feed/atom/) \
[Securelist](https://securelist.com/feed/) \
[Sophos](https://news.sophos.com/en-us/category/security-operations/feed/) \
[Hackers News](https://feeds.feedburner.com/TheHackersNews?format=xml) \
[Talos Intelligence](http://feeds.feedburner.com/feedburner/Talos) \
[Zero Day Initiative](https://www.zerodayinitiative.com/blog?format=rss) \
[DarkNet](http://www.darknet.org.uk/feed/) \
[CIS](https://www.cisecurity.org/feed/advisories) \
[US-Cert Advisories](https://us-cert.cisa.gov/ics/advisories/advisories.xml) \
[US-Cert Alerts](https://us-cert.cisa.gov/ncas/alerts.xml) \
[Ars Technica](https://arstechnica.com/tag/security/feed/) \
[Dark Reading](https://www.darkreading.com/rss/all.xml) \
[Hackmageddon](https://www.hackmageddon.com/feed/) \
[HackRead](https://www.hackread.com/feed/) \
[Infosecurity Magazine](http://www.infosecurity-magazine.com/rss/news/) \
[Cloudflare Security](https://blog.cloudflare.com/tag/security/rss) \
[Google Online Security](https://googleonlinesecurity.blogspot.com/atom.xml) \
[Google Project Zero](https://googleprojectzero.blogspot.com/feeds/posts/default) \
[Microsoft Security Blog](https://www.microsoft.com/security/blog/feed/) \
[Naked Security](https://nakedsecurity.sophos.com/feed/) \
[SOC Prime](https://socprime.com/blog/feed/) \
[Unit42](http://researchcenter.paloaltonetworks.com/unit42/feed/) \
[Checkpoint](https://research.checkpoint.com/category/threat-research/feed/) \
[SecPod](https://www.secpod.com/blog/feed/) \
[Wiz](https://www.wiz.io/feed/tag/security/rss.xml) \
[Morphisec](https://www.morphisec.com/feed/?post_type=blog)


## Environment
For this I like to use Python and Linux. The key is that it needs to be public facing so the Telegram bot can connect to it. For me, I like to use the Oracle Cloud Free Tier. With their ARM Ampere A1 Instances you get a total of 4 OCPUs and 24 GB of RAM as well as 200 GB of storage. You also get 10 TB of outbound data transfer a month. All of these specs are higher than the other popular cloud services. The catch is the fact that its so popular, when trying to setup the ARM instance, it likely wont be able to do it and it will ask you to try later. However, if you sign up for the Pay As You Go option, I have found in my own instance they will not charge you anything if you stay within those free tier limits. This option almost always let's you create it instantly and not have to try later. As this is public facing, I use it for my Telegram bots.

First, make sure Python is installed as well as the Python Virtual Environment
```
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y
```
Make a directory, CD to it and create a virtual environment
```
python3 -m venv rssbot_env
source rssbot_env/bin/activate
```
Next we Install Python packages
```
pip3 install telethon feedparser aiohttp
```
1. telethon - Telegram API client
2. feedparser - RSS feed parsing
3. aiohttp - async HTTP requests

## Telegram Bot Creation
1. When in Telegram, search for @botfather
2. Type /newbot
3. Name your bot
4. It will then ask you to make a username that has to end in _bot. You may have to try multiple times if the name is already taken.
5. Once complete you will see a message telling you the link to your Bot as well as your Bot ID. Note this down as it will be needed for the script.
6. Another thing the script will need is your api_id and api_hash. You get this by creating a Telegram app, and don't worry your not coding anything, you just need to make an empty app of some sort. 

The steps for this are as follows:
1. Go to https://my.telegram.org/ Enter your phone number in the international format (e.g., +1234567890).
2. Telegram will send a confirmation code to your Telegram app (not via SMS). Copy that code and enter it on the website to sign in. It will be the chat titled Telegram.
3. Once logged in, click on the link for "API development tools."
4. You will see a "Create new application" form. You only need to fill out the first two fields:
* App title: Give it a name (e.g., "MyTestApp").
* App short name: A shorter version (e.g., "testapp").
5. You can leave the URL and Description fields blank or use placeholders.
6. Click Create application. Your App api_id and App api_hash will appear on the next screen
 

## Script
Create a Python script called rss_bot.py. Under Configuration, fill out those 3 required fields. Also put in the list of your RSS feeds.
```
import asyncio
import feedparser
from telethon import TelegramClient, events

# ==== CONFIGURATION ====
api_id = YOUR_API_ID           # Get this from https://my.telegram.org
api_hash = 'YOUR_API_HASH'     # Get this from https://my.telegram.org
bot_token = 'YOUR_BOT_TOKEN'   # From @BotFather

# List of RSS feed URLs to monitor
rss_feeds = [
    'https://example.com/feed.xml',
    'https://another.com/rss'
]

max_articles = 10  # Number of articles to fetch per feed

# Optional keyword filtering (leave empty list to fetch all)
keywords = ['ransomware', 'leak', 'APT']

# Set to track links already sent in this session
sent_links = set()

# ==== TELETHON CLIENT ====
client = TelegramClient('rss_bot_session', api_id, api_hash)

# ==== COMMAND HANDLER ====
@client.on(events.NewMessage(pattern='/fetch'))
async def fetch_feeds(event):
    """Responds to /fetch command by sending latest RSS articles."""
    await event.respond("🔄 Fetching latest articles…")
    total_count = 0

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        # Only take the latest `max_articles` entries
        for entry in feed.entries[:max_articles]:
            link = entry.link
            title = entry.title

            # Skip if we've already sent this link
            if link in sent_links:
                continue

            # Apply keyword filter if configured
            if keywords:
                if not any(k.lower() in title.lower() for k in keywords):
                    continue

            # Prepare and send message
            message = f"**{title}**\n{link}"
            await event.respond(message, parse_mode='markdown')
            sent_links.add(link)
            total_count += 1

    await event.respond(f"✅ Done fetching feeds! {total_count} new articles sent.")

# ==== MAIN FUNCTION ====
async def main():
    await client.start(bot_token=bot_token)
    print("🤖 Bot is running. Send /fetch to pull latest RSS articles.")
    await client.run_until_disconnected()

# ==== ENTRY POINT ====
if __name__ == "__main__":
    asyncio.run(main())
```

Let's break down what this script is doing in sections:
```
import asyncio
import feedparser
from telethon import TelegramClient, events
```

1. import asyncio - This brings in Python’s asynchronous programming tools, which let the bot do multiple things at once (like waiting for a command and fetching feeds) without freezing.
2. import feedparser - This is a library that reads RSS feeds and turns them into Python data you can use.
3. from telethon import TelegramClient, events - Telethon is a library that lets us talk to Telegram.
4. TelegramClient - the "bot account" that connects to Telegram.
5. events - lets us listen for things like messages or commands.

```
# ==== CONFIGURATION ====
api_id = YOUR_API_ID           # Get this from https://my.telegram.org
api_hash = 'YOUR_API_HASH'     # Get this from https://my.telegram.org
bot_token = 'YOUR_BOT_TOKEN'   # From @BotFather
```
These three pieces of information are like keys to log your bot into Telegram. Without these, the bot can't send or receive messages.
1. api_id and api_hash - identify your Telegram account to the API.
2. bot_token - tells Telegram which bot you’re controlling.

```
# List of RSS feed URLs to monitor
rss_feeds = [
    'https://example.com/feed.xml',
    'https://another.com/rss'
]
```

This is a list of RSS feeds your bot will check when you run /fetch. Each URL points to a feed from a website. You can add more feeds here.


```
max_articles = 10  # Number of articles to fetch per feed
```
This sets how many articles your bot will grab from each feed when you run /fetch. In our case, it’s 10. You can increase or decrease this number.

```
# Optional keyword filtering (leave empty list to fetch all)
keywords = ['ransomware', 'leak', 'APT']
```
This is a list of words to filter articles. The bot will only send articles whose titles contain one of these words. If you leave this list empty (keywords = []), it will send all articles.


```
# Set to track links already sent in this session
sent_links = set()
```
This is a memory of links already sent during this run of the bot. A "set" is like a list that doesn't allow duplicates. This prevents the bot from sending the same article multiple times in one session.

```
# ==== TELETHON CLIENT ====
client = TelegramClient('rss_bot_session', api_id, api_hash)
```
This creates the connection to Telegram using Telethon. Think of this as logging your bot into Telegram.
1. 'rss_bot_session' - the name of the file that stores your login info.
2. api_id and api_hash - we use them to authenticate.


```
# ==== COMMAND HANDLER ====
@client.on(events.NewMessage(pattern='/fetch'))
async def fetch_feeds(event):
```
1. @client.on(...) - This tells the bot: “When you see a new message matching /fetch, run this function.”
2. async def fetch_feeds(event): - Defines a function (a block of code that runs when called).
3. async means the function is asynchronous, so it won’t freeze the bot.
4. event represents the incoming command message.


```
await event.respond("🔄 Fetching latest articles…")
```
1. await - tells Python to wait for this action to complete without stopping the rest of the bot.
2. event.respond(...) - sends a reply to the user who typed /fetch.
3. So the bot immediately says: “Fetching latest articles…” as a response.


```
total_count = 0
```
Initializes a counter to track how many articles we send during this /fetch command.


```
for feed_url in rss_feeds:
  feed = feedparser.parse(feed_url)
```
1. for feed_url in rss_feeds: - loops through each RSS feed in our list.
2. feedparser.parse(feed_url) - downloads the feed and converts it into a format Python can read.


```
for entry in feed.entries[:max_articles]:
   link = entry.link
   title = entry.title
```
1. feed.entries - a list of articles from the RSS feed.
2. [:max_articles] - only take the first max_articles (e.g., 10).
3. entry.link - URL of the article.
4. entry.title - title of the article.


```
if link in sent_links:
 continue
```
Checks if we already sent this article in the current session. If yes, continue, skip this article and move to the next one.


```
if keywords:
 if not any(k.lower() in title.lower() for k in keywords):
   continue
```
1. If keywords list is not empty, this checks whether the article title contains any of the keywords.
2. k.lower() in title.lower() makes the check case-insensitive.
3. If the article doesn’t match, it’s skipped.


```
message = f"**{title}**\n{link}"
await event.respond(message, parse_mode='markdown')
sent_links.add(link)
total_count += 1
```
1. message = f"...{title}...\n{link}" - formats the message to include the title in bold and the URL below.
2. await event.respond(...) - sends the message to the user.
3. sent_links.add(link) - remembers that this article has been sent.
4. total_count += 1 - adds 1 to the total number of articles sent in this /fetch.


```
await event.respond(f"✅ Done fetching feeds! {total_count} new articles sent.")
```
Sends a final message letting the user know how many articles were actually sent.


```
# ==== MAIN FUNCTION ====
async def main():
    await client.start(bot_token=bot_token)
    print("🤖 Bot is running. Send /fetch to pull latest RSS articles.")
    await client.run_until_disconnected()
```
1. async def main(): - defines the main function of the program.
2. await client.start(bot_token=bot_token) - logs the bot in using the token.
3. print(...) - shows a message in your terminal so you know the bot is running.
4. await client.run_until_disconnected() - keeps the bot listening for commands forever.


```
# ==== ENTRY POINT ====
if __name__ == "__main__":
    asyncio.run(main())
```
1. This tells Python: "If you run this file, start the main function asynchronously."
2. asyncio.run(main()) - starts the bot and keeps it alive until you stop it.


## Run the Bot Script
You can run it directly to test it
```
python3 rss_bot.py
```
It should hang there and say the bot is running. Go to your Telegram and your Bot channel and send /fetch. This should pull the last 10 articles (if you made the keywords list blank)

If all worked successfully, stop the script. You now want to background this so that if your VM cloud session disconnects it will still be running 24/7. To do this we can use a tool called 'screen'

```
sudo apt install screen -y
```
To start a new session:
```
screen -S rssbot
```
You then run your script
```
python3 rss_bot.py
```
Detach from the session (leave it running) by doing Ctrl + A, then D. To reattach:
```
screen -r rssbot
```

You now have a 24/7 RSS Feed Reader!

















































