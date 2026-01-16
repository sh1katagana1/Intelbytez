# Opensquat Daily Run

***

## Goal
I want Opensquat to run against a list of domain keywords I supply it every morning at 7 AM Central. Opensquat is a tool https://github.com/atenreiro/opensquat that will permutate keywords and look for them in newly registered domains lists as well as some phishing lists to see if any of them are similar to your keyword. Its a tool looking for domain infringement typosquats.

## What is cron?
For something to be scheduled to run, I would use cron in Linux. Cron is a scheduler, that’s it. Its job is to run commands for you automatically at specific times. In my case, I am telling cron everyday at 7 AM, run a specific script. On Ubuntu, cron starts automatically when the server boots. It checks the time every minute. If the current time matches a schedule, it runs the command. 

You give cron a schedule line in something called a crontab. A crontab is a small text file that contains scheduled jobs. There is one job per line and each user has their own crontab. To open yours, you type in:
```
crontab -e
```
The -e is for edit. It may ask you what editor you want to use, like nano or whatever you have installed. If you’ve never used cron before, it will look empty except for comments. That’s normal. A cronjob looks like this:
```
minute hour day month weekday command
```
As an example:
```
0 7 * * * /home/ubuntu/osint/opensquat/run_opensquat.sh
```
That line is basically saying "At 7:00 AM every day, run this script.". Let's break down each section.

0 - Run when the minute is 00
7 - Run at 7 AM (24-hour clock, so 7 PM is 19)
* - * means every this one is for Day of the Month (1-31)
* - This one is for Month(1-12)
* - This one is for Day of Week(0-7)
/home/ubuntu/osint/opensquat/run_opensquat.sh - This is the path to the script that contains the commands I want to run. Make sure to always use absolute paths. 

## Environment
I am running an Ubuntu machine inside of Oracle cloud. They use UTC time, so I need to set it to central Time
```
sudo timedatectl set-timezone America/Chicago
```
Then run this command to verify that the date and time is correct:
```
date
```

## Script
Go to your opensquat directory and create a virtual environment called venv and do all required pip installs for Opensquat. Then create a script called run_opensquat.sh
```
#!/bin/bash

# Absolute paths only (cron requires this)
BASE_DIR="/home/ubuntu/osint/opensquat"
VENV_DIR="$BASE_DIR/venv"
PYTHON="$VENV_DIR/bin/python"
SCRIPT="$BASE_DIR/opensquat.py"
KEYWORDS="$BASE_DIR/keywords.txt"

# Optional: log file for debugging
LOGFILE="$BASE_DIR/cron.log"

cd "$BASE_DIR" || exit 1

# Run Opensquat
"$PYTHON" "$SCRIPT" -k "$KEYWORDS" >> "$LOGFILE" 2>&1
```
Make the script executable:
```
chmod +x /home/ubuntu/osint/opensquat/run_opensquat.sh
```
Do not activate the virtual environment and test the script to verify that it does activate the virtual environment and runs Opensquat
```
./run_opensquat.sh
```
If successful you will see a results.txt file as well as a cron.log that shows the output of the command run. Let's breakdown the script:
```
#!/bin/bash
```
This line tells Linux: "Use Bash to run this file." /bin/bash is the Bash shell.

```
# Absolute paths only (cron requires this)
```
Anything starting with # is a comment. Comments are ignored by the computer. They are just for you to know what this section of script is doing.

```
BASE_DIR="/home/ubuntu/osint/opensquat"
```
This creates a variable. BASE_DIR now stands for that folder path. Its good so I dont have to keep repeating the path over and over again. 

```
VENV_DIR="$BASE_DIR/venv"
```
This builds on the previous variable. $BASE_DIR gets replaced with its value. /home/ubuntu/osint/opensquat/venv is where my python virtual environment files live in that directory.

```
PYTHON="$VENV_DIR/bin/python"
```
Instead of me running the normal source venv/bin/activate then python opensquat.py, this is doing venv/bin/python opensquat.py. Why do we do this? Cron cannot “activate” environments, so we directly use the correct Python, which is in the venv folder. It guarantees correct libraries. So the full path ends up being /home/ubuntu/osint/opensquat/venv/bin/python.

```
SCRIPT="$BASE_DIR/opensquat.py"
```
This points to the actual Opensquat program.

```
KEYWORDS="$BASE_DIR/keywords.txt"
```
This points to the keywords.txt file that by default exists in the Opensquat directory. You would modify this keyword list with the domain keywords your interested in scanning for. Dont forget, Opensquat does not take in domain names, only keywords. So not google.com, but rather google. 

```
LOGFILE="$BASE_DIR/cron.log"
```
This is where normal output and error messages will be written.

```
cd "$BASE_DIR" || exit 1
```
The cd command moves into /home/ubuntu/osint/opensquat. Some programs write output to the current directory, some do not. In the case of Opensquat, it does write to the current directory. we are just ensuring its in the directory. The || exit 1 means "If cd fails, stop immediately." Maybe the folder was deleted or permissions changed. exit 1 means: Exit with an error code and cron logs this as a failure. Essentially, you can think of it like "Go to the Opensquat directory. If that doesn’t work, stop everything."

```
"$PYTHON" "$SCRIPT" -k "$KEYWORDS" >> "$LOGFILE" 2>&1
```
"$PYTHON" expands to: /home/ubuntu/osint/opensquat/venv/bin/python, if you recall the variable we set earlier. "$SCRIPT" -k "$KEYWORDS" expands to: opensquat.py -k keywords.txt, again because of the variables we set earlier. >> "$LOGFILE" Append output to cron.log and do not overwrite existing logs. If you did a single > it would overwrite what was in there. So every run will add new lines. The 2>&1 means:
* 1 = normal output
* 2 = error output
* 2>&1 = send errors to the same place as output
This essentially says put everything in the log file. 

So in order, what should run is:
```
/home/ubuntu/osint/opensquat/venv/bin/python \
/home/ubuntu/osint/opensquat/opensquat.py \
-k /home/ubuntu/osint/opensquat/keywords.txt \
>> /home/ubuntu/osint/opensquat/cron.log 2>&1
```

## Create cronjob
Run this:
```
crontab -e
```
If its the first job you have ever created it will just have comments. Go to the end of the comments and to a new line and enter:
```
0 7 * * * /home/ubuntu/osint/opensquat/run_opensquat.sh
```
Verify your cron service is running:
```
systemctl status cron
```
You can also watch logs:
```
grep CRON /var/log/syslog
```


























