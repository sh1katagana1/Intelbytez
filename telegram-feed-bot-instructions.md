# Telegram Security Blog Feed Reader Bot

***

## Goal
I want to create a self local hosted telegram bot that lets my use /latest to pull the latest 10 articles from https://www.bleepingcomputer.com/feed/

This requires three main steps:
1. Create your Telegram bot and get a token: Message @BotFather in Telegram, use /newbot, give it a name, and note your Bot Token
2. Set up your Python environment: Use libraries: python-telegram-bot (to interact with Telegram) and feedparser (to parse RSS feeds).

This approach is fully self-hosted and only requires a machine that runs Python and can access the internet

## Language
Python

## Script
```
# Requirements: python-telegram-bot, feedparser
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import feedparser

# Telegram Token from @BotFather
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
RSS_URL = "https://www.bleepingcomputer.com/feed/"

def latest(update: Update, context: CallbackContext):
    feed = feedparser.parse(RSS_URL)
    articles = feed.entries[:10]
    messages = [
        f"{i+1}. [{entry.title}]({entry.link})"
        for i, entry in enumerate(articles)
    ]
    update.message.reply_text('\n'.join(messages), parse_mode='Markdown')

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("latest", latest))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
```
Replace YOUR_TELEGRAM_BOT_TOKEN with your actual token. This bot uses polling, so you don’t need to open any ports on your local network

## How it works:
1. When you send /latest, it replies with the 10 most recent article titles and links from the BleepingComputer RSS feed.
2. If you run this on your own machine, only you (and users you share the bot link with) can use it.
3. The polling method means it’s accessible from anywhere you’re logged in, without exposing your network

## Error
I found trying this that I get this error: 
```
Traceback (most recent call last):
  File "/root/telegram/bots/bleepingbot/bleepingbot.py", line 27, in <module>
    main()
    ~~~~^^
  File "/root/telegram/bots/bleepingbot/bleepingbot.py", line 20, in main
    updater = Updater(TELEGRAM_TOKEN)
TypeError: Updater.__init__() missing 1 required positional argument: 'update_queue'
```
The error is due to a major version change in the python-telegram-bot library. In python-telegram-bot version 20.x and newer, the API has changed significantly and the Updater class no longer works as in older versions. The constructor now requires different arguments or is no longer meant to be used for new bots, as the recommended method is to use the new Application framework

## How to fix:
1. Recommended: Update your code to use the new Application API (best practice and supported for recent python-telegram-bot versions).
2. Alternative: Downgrade to an older version (v13.x) if you want to keep your existing code (not recommended due to EOL and lack of updates).

I will update my Bot for v20+ 
```
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
RSS_URL = "https://www.bleepingcomputer.com/feed/"

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feed = feedparser.parse(RSS_URL)
    articles = feed.entries[:10]
    messages = [
        f"{i+1}. [{entry.title}]({entry.link})"
        for i, entry in enumerate(articles)
    ]
    await update.message.reply_text('\n'.join(messages), parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("latest", latest))
    app.run_polling()

if __name__ == "__main__":
    main()
```
## Changes  
1. Handler functions are now async (hence async def latest and using await).
2. Initialization uses ApplicationBuilder.

## Modification 1
I want to modify this to include the following feeds: https://feeds.feedburner.com/TheHackersNews?format=xml  and https://www.darkreading.com/rss.xml I want to also include an intro when you start the bot that lists instructions such as: "Welcome to my feeds. Please do /latest to get the latest 10 articles"

```
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
from datetime import datetime

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
RSS_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews?format=xml",
    "https://www.darkreading.com/rss.xml"
]

# Helper to parse and merge all feeds
def fetch_latest_articles(n=10):
    all_entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Parse date safely
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            else:
                published = datetime.now()
            all_entries.append({
                "title": entry.title,
                "link": entry.link,
                "published": published
            })
    # Sort articles by published date (desc)
    sorted_entries = sorted(all_entries, key=lambda x: x["published"], reverse=True)[:n]
    return sorted_entries

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = (
        "👋 Welcome to my feeds.\n\n"
        "Use /latest to get the 10 most recent articles across:\n"
        "- BleepingComputer\n"
        "- The Hacker News\n"
        "- DarkReading"
    )
    await update.message.reply_text(intro)

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = fetch_latest_articles()
    if not articles:
        await update.message.reply_text("No articles found.")
        return
    messages = [
        f"{i+1}. [{a['title']}]({a['link']})"
        for i, a in enumerate(articles)
    ]
    await update.message.reply_text('\n'.join(messages), parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.run_polling()

if __name__ == "__main__":
    main()
```
## Key details:
1. Intro Message: Shown on /start with brief instructions and a feed list.
2. /latest: Pulls, merges, and sorts entries from all three feeds, reliably picking the 10 most recent overall.
3. Feed additions: You only need to add more URLs to the RSS_FEEDS list to expand sources.
4. No external config files or databases are required for this basic functionality.

## Modification 2
I want to modify this to let me do /add plus a feed url to add more feeds down the line. I want to also include that /add in my intro instructions.

```
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
from datetime import datetime
import os

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
FEEDS_FILE = "feeds.txt"

DEFAULT_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews?format=xml",
    "https://www.darkreading.com/rss.xml"
]

def load_feeds():
    if not os.path.exists(FEEDS_FILE):
        with open(FEEDS_FILE, "w") as f:
            f.write("\n".join(DEFAULT_FEEDS))
    with open(FEEDS_FILE, "r") as f:
        feeds = [line.strip() for line in f if line.strip()]
    return feeds

def save_feeds(feeds):
    with open(FEEDS_FILE, "w") as f:
        for feed in feeds:
            f.write(feed + "\n")

def fetch_latest_articles(n=10):
    feeds = load_feeds()
    all_entries = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # Parse date safely
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            else:
                published = datetime.now()
            all_entries.append({
                "title": entry.title,
                "link": entry.link,
                "published": published
            })
    sorted_entries = sorted(all_entries, key=lambda x: x["published"], reverse=True)[:n]
    return sorted_entries

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = (
        "👋 Welcome to my feeds bot.\n\n"
        "Use /latest to get the 10 most recent articles from all feeds.\n"
        "Use /add <feed-url> to add an RSS feed.\n"
        "Current feeds:\n"
    )
    feeds = load_feeds()
    for f in feeds:
        intro += f"- {f}\n"
    await update.message.reply_text(intro)

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = fetch_latest_articles()
    if not articles:
        await update.message.reply_text("No articles found.")
        return
    messages = [
        f"{i+1}. [{a['title']}]({a['link']})"
        for i, a in enumerate(articles)
    ]
    await update.message.reply_text('\n'.join(messages), parse_mode='Markdown')

async def add_feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /add <feed-url>")
        return
    url = context.args[0].strip()
    feeds = load_feeds()
    if url in feeds:
        await update.message.reply_text("This feed is already added.")
        return
    # Optionally, check feed validity before adding
    feed = feedparser.parse(url)
    if not feed.entries:
        await update.message.reply_text("Couldn't fetch articles from this URL. Make sure it's a valid RSS feed.")
        return
    feeds.append(url)
    save_feeds(feeds)
    await update.message.reply_text(f"Feed added!\nNow tracking {len(feeds)} feeds.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("add", add_feed))
    app.run_polling()

if __name__ == "__main__":
    main()
```
## Summary of changes:
1. RSS feeds persist in feeds.txt.
2. /add <url> will add a unique, valid RSS feed.
3. Intro message now describes /add and lists current feeds.
4. You'll need write permission in the folder for feeds.txt.

## Modification 3
I want to modify where I can type in /list and get a list of all current feeds im monitoring. I want to also add /list to my intro instructions. I want to also change when i do /latest to have a separate section for each feeds last 10 articles.

```
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
from datetime import datetime
import os

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
FEEDS_FILE = "feeds.txt"

DEFAULT_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews?format=xml",
    "https://www.darkreading.com/rss.xml"
]

def load_feeds():
    if not os.path.exists(FEEDS_FILE):
        with open(FEEDS_FILE, "w") as f:
            f.write("\n".join(DEFAULT_FEEDS))
    with open(FEEDS_FILE, "r") as f:
        feeds = [line.strip() for line in f if line.strip()]
    return feeds

def save_feeds(feeds):
    with open(FEEDS_FILE, "w") as f:
        for feed in feeds:
            f.write(feed + "\n")

def fetch_feed_articles(url, n=10):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:n]:
        # Parse date safely
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        else:
            published = datetime.now()
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": published
        })
    return articles, feed.feed.title if hasattr(feed.feed, "title") else url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = (
        "👋 Welcome to my feeds bot.\n\n"
        "Commands:\n"
        "• /latest — Show the latest 10 articles for each feed\n"
        "• /add <feed-url> — Add a new RSS feed\n"
        "• /list — List all currently monitored feeds\n"
        "\nCurrent feeds:\n"
    )
    feeds = load_feeds()
    for f in feeds:
        intro += f"- {f}\n"
    await update.message.reply_text(intro)

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feeds = load_feeds()
    msg_chunks = []
    for url in feeds:
        articles, title = fetch_feed_articles(url)
        section = f"*{title}*\n"
        if articles:
            section += "\n".join(
                f"{i+1}. [{a['title']}]({a['link']})"
                for i, a in enumerate(articles)
            )
        else:
            section += "_No articles found._"
        msg_chunks.append(section)
    # Assemble the full message - send as multiple messages if too long (Telegram's 4096 char limit)
    for chunk in msg_chunks:
        await update.message.reply_text(chunk, parse_mode='Markdown')

async def list_feeds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feeds = load_feeds()
    if not feeds:
        await update.message.reply_text("No feeds are currently being monitored.")
        return
    msg = "*Currently monitored feeds:*\n"
    for f in feeds:
        msg += f"- {f}\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def add_feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /add <feed-url>")
        return
    url = context.args[0].strip()
    feeds = load_feeds()
    if url in feeds:
        await update.message.reply_text("This feed is already added.")
        return
    # Validate feed before adding
    feed = feedparser.parse(url)
    if not feed.entries:
        await update.message.reply_text("Couldn't fetch articles from this URL. Make sure it's a valid RSS feed.")
        return
    feeds.append(url)
    save_feeds(feeds)
    await update.message.reply_text(f"Feed added!\nNow tracking {len(feeds)} feeds.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("add", add_feed))
    app.add_handler(CommandHandler("list", list_feeds))
    app.run_polling()

if __name__ == "__main__":
    main()
```
## Usage summary:
1. /start: Shows intro, instructions, and currently tracked feeds.
2. /add <feed-url>: Adds a new RSS feed (if valid).
3. /list: Lists all current feeds.
4. /latest: Shows the latest 10 entries for each feed as its own section.

## Modification 4
I want to modify to let me type /remove then url of the feed and it will remove this feed from my list

```
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
from datetime import datetime
import os

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
FEEDS_FILE = "feeds.txt"

DEFAULT_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews?format=xml",
    "https://www.darkreading.com/rss.xml"
]

def load_feeds():
    if not os.path.exists(FEEDS_FILE):
        with open(FEEDS_FILE, "w") as f:
            f.write("\n".join(DEFAULT_FEEDS))
    with open(FEEDS_FILE, "r") as f:
        feeds = [line.strip() for line in f if line.strip()]
    return feeds

def save_feeds(feeds):
    with open(FEEDS_FILE, "w") as f:
        for feed in feeds:
            f.write(feed + "\n")

def fetch_feed_articles(url, n=10):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:n]:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])
        else:
            published = datetime.now()
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": published
        })
    return articles, feed.feed.title if hasattr(feed.feed, "title") else url

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = (
        "👋 Welcome to my feeds bot.\n\n"
        "Commands:\n"
        "• /latest — Show the latest 10 articles for each feed\n"
        "• /add <feed-url> — Add a new RSS feed\n"
        "• /remove <feed-url> — Remove a tracked RSS feed\n"
        "• /list — List all currently monitored feeds\n"
        "\nCurrent feeds:\n"
    )
    feeds = load_feeds()
    for f in feeds:
        intro += f"- {f}\n"
    await update.message.reply_text(intro)

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feeds = load_feeds()
    msg_chunks = []
    for url in feeds:
        articles, title = fetch_feed_articles(url)
        section = f"*{title}*\n"
        if articles:
            section += "\n".join(
                f"{i+1}. [{a['title']}]({a['link']})"
                for i, a in enumerate(articles)
            )
        else:
            section += "_No articles found._"
        msg_chunks.append(section)
    for chunk in msg_chunks:
        await update.message.reply_text(chunk, parse_mode='Markdown')

async def list_feeds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feeds = load_feeds()
    if not feeds:
        await update.message.reply_text("No feeds are currently being monitored.")
        return
    msg = "*Currently monitored feeds:*\n"
    for f in feeds:
        msg += f"- {f}\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def add_feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /add <feed-url>")
        return
    url = context.args[0].strip()
    feeds = load_feeds()
    if url in feeds:
        await update.message.reply_text("This feed is already added.")
        return
    feed = feedparser.parse(url)
    if not feed.entries:
        await update.message.reply_text("Couldn't fetch articles from this URL. Make sure it's a valid RSS feed.")
        return
    feeds.append(url)
    save_feeds(feeds)
    await update.message.reply_text(f"Feed added!\nNow tracking {len(feeds)} feeds.")

async def remove_feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /remove <feed-url>")
        return
    url = context.args[0].strip()
    feeds = load_feeds()
    if url not in feeds:
        await update.message.reply_text("This feed URL is not in the monitored list.")
        return
    feeds.remove(url)
    save_feeds(feeds)
    await update.message.reply_text(f"Feed removed!\nNow tracking {len(feeds)} feeds.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("add", add_feed))
    app.add_handler(CommandHandler("list", list_feeds))
    app.add_handler(CommandHandler("remove", remove_feed))
    app.run_polling()

if __name__ == "__main__":
    main()
```
## Summary of additions:
1. /remove <feed-url> removes the given feed URL if it exists.
2. Confirmation messages for removal or if the feed URL was not found.
3. Updated /start intro to mention the new /remove command.
4. No other changes necessary.

