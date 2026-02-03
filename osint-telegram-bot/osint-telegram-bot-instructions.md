# OSINT Telegram Bot

***

# https://t.me/shikataosint2026_bot

## Goal
To make an OSINT bot in Telegram that will run tools I have in an Ubuntu VM, as well as online sources

## Environment
Telegram
Ubuntu VM using Oracle Pay As You Go Setup with Free Tier limits of 24GB RAM, 4 core CPU and 150 GB of hard drive space

## The plan:
1. Runs 24/7 on your Oracle Ubuntu VM
2. Listens for commands in Telegram (
3. Runs local OSINT tools + online APIs
4. Collects results
5. Sends them back as downloadable files

## Username Test
In the first version of this I want to try creating the bot to feed it a username, which will trigger Maigret to run on my Ubuntu and give me back results. Ill add online API source capability as well.

## Setup
So to start I make my folder called osint-telegram-bot. I then create a python virtual environment where the tools will lay
```
python3 -m venv venv
```
I then activate it
```
source venv/bin/activate
```
I install the telegram dependency
```
pip3 install python-telegram-bot==20.7
```
You can test its properly working with:
```
python3 -c "import telegram; print(telegram.__version__)"
```
I install pipx and maigret. 
```
sudo apt install -y pipx
pipx ensurepath
pipx install maigret
```
Test by running
```
maigret --help
```
I did initially run into some pathing issues with this. I did a few steps.

I manually sourced my shell configuration
```
source ~/.bashrc
```
Then again tried
```
maigret --help
```
If that doesnt work, try exiting the shell and doing a new one
```
exit
ssh ubuntu@your_vm_ip
```
You can check by doing
```
ls -l ~/.local/bin/maigret
```
You should see
```
/home/ubuntu/.local/bin
```
You also need to go to Telegram and search for Botfather. You create a new bot by using /newbot and follow the instructions. At the end you will get a Bot Token and a URL to your bot. Write these down for later.


## Folder Creation
The structure of folders and files I created are as such:
```
osint-telegram-bot/
├── bot.py
├── config.py
├── modules/
│   ├── username/
│   └── email/
├── output/
└── venv/
```
I put a placeholder for email searches as well.

## Bot.py
This is the main script, let's start there.
```
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from config import BOT_TOKEN, OUTPUT_DIR
from modules.username import run_all as run_username
from modules.email import run_all as run_email

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕵️ OSINT Bot Ready\n\n"
        "Commands:\n"
        "/username <name>\n"
        "/email <email>"
    )

async def username_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /username <username>")
        return

    username = context.args[0]
    await update.message.reply_text(f"🔍 Searching username: `{username}`", parse_mode="Markdown")

    filepath = run_username(username, OUTPUT_DIR)

    await update.message.reply_document(
        document=open(filepath, "rb"),
        filename=os.path.basename(filepath)
    )

async def email_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /email <email>")
        return

    email = context.args[0]
    await update.message.reply_text(f"📧 Searching email: `{email}`", parse_mode="Markdown")

    filepath = run_email(email, OUTPUT_DIR)

    await update.message.reply_document(
        document=open(filepath, "rb"),
        filename=os.path.basename(filepath)
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("username", username_cmd))
    app.add_handler(CommandHandler("email", email_cmd))

    print("[+] OSINT Telegram Bot running")
    app.run_polling()

if __name__ == "__main__":
    main()
```
What does it do?
1. Connects to Telegram
2. Registers commands (/start, /username, /email)
3. Calls the correct OSINT module
4. Sends results back as files

```
import os
```
You are importing Python’s built-in operating system tools. This lets Python:
1. Work with folders
2. Create directories
3. Handle file paths

It's needed because later, you create the output/ folder if it doesn’t exist.

```
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
```
You are importing tools from the python-telegram-bot library.

An Update is: "One thing that happened on Telegram" Examples:
1. A message
2. A command
3. A photo
4. A button press
5. In our case an Update = someone typed /username testuser

ApplicationBuilder
1. Creates the Telegram bot
2. Connects it to Telegram’s servers
3. Keeps listening for messages
4. Think of it as "Start the Telegram engine"

CommandHandler links a command (like /email) to a Python function. Example:
```
CommandHandler("email", email_cmd)
```
Means "When /email is typed, run email_cmd()"

ContextTypes holds:
1. Arguments
2. Metadata
3. Session info

```
from config import BOT_TOKEN, OUTPUT_DIR
```
This is importing your own files. You are importing variables from your own file (config.py).
1. BOT_TOKEN → Telegram authentication
2. OUTPUT_DIR → where results are saved


```
from modules.username import run_all as run_username
from modules.email import run_all as run_email
```
You are importing functions from your modules. These mean "Import run_all, but rename it to run_username here"

```
os.makedirs(OUTPUT_DIR, exist_ok=True)
```
This means create the output/ directory only if it doesn’t already exist. If it already exists, don’t crash. This is because systemd may start the bot before you manually create folders.

```
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
```
This is for when you do /start in your Telegram bot chat. 
1. def - define a function
2. async - this function can pause without blocking others

Async is important because Telegram bots handle multiple messages. Async prevents freezing

3. Update - The message that was sent
4. Context - Extra data (arguments, metadata)

```
await update.message.reply_text(
```
It means "Wait for this to finish, but don’t block the bot". This sends a message back to Telegram.

```
"🕵️ OSINT Bot Ready\n\n"
"Commands:\n"
"/username <name>\n"
"/email <email>"
```
This is just text formatting. You see this when you type /start in the bot channel. Its where you give instructions for how to use your bot. 

```
async def username_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
```
This runs when someone types /username in the Telegram bot.

```
if not context.args:
```
This means "If no arguments were given". This would be like if i did /username but didnt supply a username. If no argument given then it runs:
```
await update.message.reply_text("Usage: /username <username>")
return
```
The function exits early.


```
username = context.args[0]
```
If you typed in /username leroyjenkins, then this code would be:
```
username == "leroyjenkins"
```

```
await update.message.reply_text(
    f"🔍 Searching username: `{username}`",
    parse_mode="Markdown"
)
```
This lets the user know work is happening. Uses Markdown formatting for backticks


```
filepath = run_username(username, OUTPUT_DIR)
```
This line:
1. Calls your username module
2. Runs Maigret + web sources
3. Writes a file
4. Returns the file path


```
await update.message.reply_document(
    document=open(filepath, "rb"),
    filename=os.path.basename(filepath)
)
```
This is to send the results file back to Telegram
1. Open file in binary mode ("rb")
2. Send it as a downloadable document
3. Telegram handles delivery


```
filepath = run_email(email, OUTPUT_DIR)
```
Conceptually the same as the username one.


```
def main():
```
This is the entry point. First, systemd runs:
```
python bot.py
```
Python looks for:
```
if __name__ == "__main__":
```
And calls main().


```
app = ApplicationBuilder().token(BOT_TOKEN).build()
```
This creates the bot application.
1. Authenticates with Telegram
2. Creates the bot
3. Prepares event loop


```
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("username", username_cmd))
app.add_handler(CommandHandler("email", email_cmd))
```
This tells the bot which commands exist and which functions handle them.


```
app.run_polling()
```
1. Connects to Telegram
2. Polls for updates
3. Runs forever


```
if __name__ == "__main__":
    main()
```
This means "Only run main() if this file is executed directly"



## Config.py
```
BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN"

OUTPUT_DIR = "output"

EMAILREP_API_KEY = "PASTE_EMAILREP_KEY"
HUNTER_API_KEY = "PASTE_HUNTER_KEY"
BREACHVIP_API_KEY = "PASTE_BREACHVIP_KEY"
```

This is where you put some variable values in. I have a few extra placeholders here. 


## Maigret_provider.py
```
import subprocess

MAIGRET_PATH = "/home/ubuntu/.local/bin/maigret"

def run(username):
    cmd = [
        MAIGRET_PATH,
        username,
        "--no-color",
        "--timeout", "15"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    return (
        "===== MAIGRET RESULTS =====\n\n"
        + result.stdout
        + "\n"
    )
```
This is for running the maigret username OSINT tool.

```
import subprocess
```
1. Imports Python’s built-in tool for running external programs
2. Lets Python act like a terminal

Think of subprocess being like "Open a terminal, run a command, capture what it prints"


```
MAIGRET_PATH = "/home/ubuntu/.local/bin/maigret"
```
When I originally installed Maigret, it was just at maigret, not the full absolute path. Once you add this bot as a systemd service, it will want the full absolute path, so we did that here. This is because systemd does NOT know your PATH and does NOT read .bashrc. 


```
def run(username):
```
Dont forget we saw this back in our main bot.py in the import section. Here we are defining a function called run. 
1. Takes one input: username
2. Returns text output


```
cmd = [
    MAIGRET_PATH,
    username,
    "--no-color",
    "--timeout", "15"
]
```
This is a Python list where each item is one part of the terminal command. It would as if I typed this in the terminal:
```
/home/ubuntu/.local/bin/maigret username --no-color --timeout 15
```
Lists are safer to use than strings for command injection mitigations. 
1. MAIGRET_PATH	Program to run
2. username	Target username
3. --no-color	Remove ANSI color codes
4. --timeout 15	Don’t hang forever


```
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True
)
```
This runs Maigret. 
1. Starts Maigret
2. Waits for it to finish
3. Captures everything it prints

The parameters are as follows:
1. cmd - The command list we built earlier.
2. capture_output=True - Means "Save stdout and stderr instead of printing to screen"
3. text=True - Means "Treat output as text, not raw bytes"

So here is what results outputs, and we are using the stdout one:
```
result.stdout   # normal output
result.stderr   # error output
result.returncode  # exit code (0 = success)
```


```
return (
    "===== MAIGRET RESULTS =====\n\n"
    + result.stdout
    + "\n"
)
```
This makes the final report readable.
1. Adds a header
2. Appends Maigret’s output
3. Adds a newline

We are writing to file because Telegram chats have a character limit. As Maigret may exceed that limit, we will just get the results as a text file instead of inside the chat.


## __init__.py
```
import os
from datetime import datetime

from .maigret_provider import run as maigret
from .web_provider import run as web

def run_all(username, output_dir):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"username_{username}_{ts}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("USERNAME OSINT REPORT\n")
        f.write(f"Target: {username}\n")
        f.write(f"Generated: {ts}\n\n")

        f.write(maigret(username))
        f.write("\n")
        f.write(web(username))

    return filepath
```

__init__.py turns a folder into a Python module. Without it Python treats the folder as "just files" and you cannot import from it cleanly. Because this file exists, you can do this in bot.py:
```
from modules.username import run_all
```
That is the entire purpose of this file, to act as the public interface of the module.

```
import os
```
This imports Python’s operating system helper library. You need it to:
1. Build file paths correctly
2. Avoid hardcoding / characters

```
from datetime import datetime
```
Imports the datetime class, which lets Python:
1. Get the current date & time
2. Format it as text
3. Use it to timestamp output files and prevent filename collisions


```
from .maigret_provider import run as maigret
from .web_provider import run as web
```
We know the maigret_provider one from earlier, and I put a placeholder for a soon to be created web_provider one for online APIs. The dot (.) means "Look in the same folder as this file". 

Inside maigret_provider.py, there is a function called:
```
def run(username):
```
So here in the import command we see:
```
from .maigret_provider import run as maigret
```
Which means import the function run, but rename it to maigret. We may have multiple providers that have a run() function. We do the renaming to avoid confusion.

```
def run_all(username, output_dir):
```
This defines a function called run_all. Think of it as the manager. This function:
1. Is the main entry point for username searches
2. Is what bot.py calls
3. Coordinates everything


```
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
```
1. datetime.now() - Gets the current date & time.
2. .strftime(...) - Formats it as text.

The format would look like
```
20260202_154530
```

```
filename = f"username_{username}_{ts}.txt"
```
This builds the filename of the file that gets sent to Telegram. This is an f-string and it inserts variables into text. The code here would then look like:
```
username_testuser_20260202_154530.txt
```
In Telegram once sent to it.


```
filepath = os.path.join(output_dir, filename)
```
This builds the full file path. It combines:
1. Output directory (output/)
2. Filename

The result would be:
```
output/username_testuser_20260202_154530.txt
```
os.path.join() works correctly on all systems. 



```
with open(filepath, "w", encoding="utf-8") as f:
```
1. Opens the file for writing ("w")
2. Creates it if it doesn’t exist
3. Ensures it closes automatically
4. The with keyword means "When we’re done, close the file safely"
5. This prevents file corruption.


```
f.write("USERNAME OSINT REPORT\n")
f.write(f"Target: {username}\n")
f.write(f"Generated: {ts}\n\n")
```
This will write:
```
USERNAME OSINT REPORT
Target: leroyjenkins
Generated: 20260202_154530
```

```
f.write(maigret(username))
```
1. Calls the Maigret provider
2. Runs the Maigret program
3. Captures its output
4. Writes it to the file

Its basically saying "Call maigret(username) and get text"

```
f.write("\n")
```
Add spacing. Prevents sections from smashing together.


```
f.write(web(username))
```
When I make the web_provider one, this will run it. You can comment out for now.


```
return filepath
```
This tells the caller (bot.py) "Here is the file I created". Without it our Bot wouldn’t know what file to send and Telegram couldn’t return results.



































































