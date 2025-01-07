# Telegram Security Feeds Puller Bot instructions

***


## Goal
To create a telegram bot, using the changes with the new python-telegram-bot library, that takes in a blog rss feed url and displays the 20 latest articles in the bot.

## Script
```
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import feedparser

# Replace 'YOUR_BOT_TOKEN' with the actual token you received from BotFather
TOKEN = 'YOUR_BOT_TOKEN'

# Replace this with the RSS feed URL you want to use
RSS_FEED_URL = 'https://example.com/rss-feed'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /latest to get the 20 latest articles.')

async def latest_articles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    feed = feedparser.parse(RSS_FEED_URL)
    articles = feed.entries[:20]  # Get the 20 latest articles

    response = "Here are the 20 latest articles:\n\n"
    for i, article in enumerate(articles, 1):
        response += f"{i}. {article.title}\n{article.link}\n\n"

    await update.message.reply_text(response)

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("latest", latest_articles))

    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main())
```

## What does this script do?
This script does the following:

1. We import the necessary modules, including asyncio for asynchronous programming, telegram and telegram.ext for the Telegram bot functionality, and feedparser for parsing the RSS feed
2. We define the TOKEN variable with your bot token and RSS_FEED_URL with the URL of the RSS feed you want to use.
3. The start function is a command handler that responds when a user starts the bot or sends the /start command.
4. The latest_articles function is the main feature of the bot. It:
5. Parses the RSS feed using feedparser
6. Extracts the 20 latest articles
7. Formats them into a message
8. Sends the message back to the user
    I
In the main function, we:
1. Create an Application instance
2. Add command handlers for /start and /latest
3. Start the bot using application.run_polling()
4. Finally, we use asyncio.run(main()) to run the asynchronous main function.

## Usage
To use this script:

1. Install the required libraries:
```
pip install python-telegram-bot feedparser
```
1. Replace 'YOUR_BOT_TOKEN' with your actual bot token.
2. Replace 'https://example.com/rss-feed' with the actual RSS feed URL you want to use.
3. Run the script.

Now, when users interact with your bot, they can use the /latest command to get the 20 latest articles from the specified RSS feed

## Modification 1
Modify the above code to fix the following error: RuntimeError: Cannot close a running event loop
sys:1: RuntimeWarning: coroutine 'Application.shutdown' was never awaited
sys:1: RuntimeWarning: coroutine 'Application.initialize' was never awaited

To fix the RuntimeError and RuntimeWarnings you're encountering, we need to modify the main function and the way we run the bot. Here's the updated code that should resolve these issues:

## Script
```
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import feedparser

TOKEN = 'YOUR_BOT_TOKEN'
RSS_FEED_URL = 'https://example.com/rss-feed'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /latest to get the 20 latest articles.')

async def latest_articles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    feed = feedparser.parse(RSS_FEED_URL)
    articles = feed.entries[:20]
    response = "Here are the 20 latest articles:\n\n"
    for i, article in enumerate(articles, 1):
        response += f"{i}. {article.title}\n{article.link}\n\n"
    await update.message.reply_text(response)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("latest", latest_articles))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
```

## What is this modification doing?
The key changes made to fix the errors are:

1. The main function is no longer async. We removed the async keyword from its definition
2. We removed await from application.run_polling(). This method is not a coroutine and should not be awaited
3. We removed asyncio.run(main()). Instead, we're directly calling main() at the end of the script
4. We removed the await application.idle() line, as it's not necessary when using run_polling()

These changes should resolve the RuntimeError about closing a running event loop and the RuntimeWarnings about coroutines never being awaited. The run_polling() method now handles the event loop internally, which simplifies our code and avoids conflicts with event loop management. Remember to replace 'YOUR_BOT_TOKEN' with your actual bot token and 'https://example.com/rss-feed' with the RSS feed URL you want to use.


## Modification 2
Modify the above code to allow me to put in as many blog rss urls as I want. We'll store these URLs in a list and add a command to let users choose which feed they want to see articles from. Here's the updated code:

## Script
```
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import feedparser

TOKEN = 'YOUR_BOT_TOKEN'

# List of RSS feed URLs. Add as many as you want.
RSS_FEEDS = [
    {'name': 'Blog 1', 'url': 'https://example1.com/rss-feed'},
    {'name': 'Blog 2', 'url': 'https://example2.com/rss-feed'},
    {'name': 'Blog 3', 'url': 'https://example3.com/rss-feed'},
    # Add more feeds here
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Use /feeds to see available RSS feeds.')

async def show_feeds(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(feed['name'], callback_data=str(i))]
        for i, feed in enumerate(RSS_FEEDS)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose a feed:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    feed_index = int(query.data)
    feed = RSS_FEEDS[feed_index]
    
    await query.edit_message_text(text=f"Fetching latest articles from {feed['name']}...")
    
    feed_data = feedparser.parse(feed['url'])
    articles = feed_data.entries[:20]
    
    response = f"Here are the 20 latest articles from {feed['name']}:\n\n"
    for i, article in enumerate(articles, 1):
        response += f"{i}. {article.title}\n{article.link}\n\n"
    
    # Split response if it's too long
    if len(response) > 4096:
        for x in range(0, len(response), 4096):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response[x:x+4096])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("feeds", show_feeds))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
```

## What does this modification do?
Here's what changed in this version:

1. We now have a RSS_FEEDS list that contains dictionaries with 'name' and 'url' for each feed. You can add as many feeds as you want to this list.
2. The /start command now informs users to use /feeds to see available RSS feeds.
3. A new /feeds command shows users a list of available feeds as inline keyboard buttons.
4. The button function handles the user's feed selection, fetches the articles from the selected feed, and sends them to the user.
5. We've added error handling to split long messages if they exceed Telegram's message length limit.

## Usage
To use this script:

1. Replace 'YOUR_BOT_TOKEN' with your actual bot token.
2. Modify the RSS_FEEDS list to include the RSS feeds you want to offer. Add as many as you like, following the format in the example.
3. Run the script.

Now, when users interact with your bot:

1. They can use /start to get started.
2. They can use /feeds to see a list of available RSS feeds.
3. They can select a feed from the list to get the 20 latest articles from that feed.

This setup allows you to easily add or remove RSS feeds by modifying the RSS_FEEDS list, without needing to change any other part of the code.