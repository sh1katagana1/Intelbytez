# Blackbird Docker Setup

***

## Description
Blackbird appears to have a Dockerfile but not an official Dockerhub like Maigret does. So we have to build this one from the Dockerfile. 

## Setup
This tutorial assumes my folder structure is this:
```
/root/osint-tools/docker-stuff/blackbird/
```
I will also create a folder called reports inside this folder. This will be so I can map the results Blackbird gets in the container  and put it here on my local machine inside that reports folder. 

## Clone Repo
```
cd /root/osint-tools/docker-stuff
git clone https://github.com/p1ngul1n0/blackbird.git
cd blackbird
```
## Build Docker Image
```
docker build -t blackbird .
```
## AI
Blackbird has an AI option that will summarize the results. To do it you need to generate a key. Because this is problematic doing it inside the container, the best way is to go to a separate folder, clone blackbird and install via a Python virtual environment. Then run:
```
python blackbird.py --setup-ai
```
This will create an api key json file. Take that file and copy it to your /root/osint-tools/docker-stuff/blackbird/ location. We will call on this later in our run command. The final result will look like: /root/osint-tools/blackbird/.ai_key.json

## Create Reports Folder
Make sure your still in /root/osint-tools/docker-stuff/blackbird/
```
mkdir -p /root/osint-tools/docker-stuff/blackbird/reports
```
Just to be safe, do this:
```
chmod 777 /root/osint-tools/docker-stuff/blackbird/reports
```

## Run The Tool
```
docker run -it --rm \
  -v /root/osint-tools/docker-stuff/blackbird/reports:/results \
  -v /root/osint-tools/docker-stuff/blackbird/.ai_key.json:/.ai_key.json:ro \
  blackbird -u username --pdf -ai
```
This will run, prompt you to agree to terms, then after it gets its results, it will do an AI summarization and print all of it to a PDF file. Let's run through these switches:

* -it  Required for AI prompts
* --rm  Cleans up container after run
* -v reports:/results  Saves PDFs to your machine
* -v .ai_key.json  Reuses your API key
* -u username  Required flag 
* --pdf  Generate report
* -ai  Enable AI analysis

As far as the -it switch goes:
* -i  Keeps stdin open
* -t  Gives you a terminal

Without this you would get an end of file error. This allows the Acknowledgement prompt that Blackbird does to pass through and let's you type in Y for yes.

## Telegram Bot Refinement
Because it prompts you during each run before it will continue, this is not efficient for when you want this to run via a Telegram Bot. To make this so its non-interactive, change your run command to this:

```
printf "y\ny\n" | docker run -i --rm \
  -v /root/osint-tools/docker-stuff/blackbird/reports:/results \
  -v /root/osint-tools/docker-stuff/blackbird/.ai_key.json:/.ai_key.json:ro \
  blackbird -u rconfer --pdf -ai
```
Let's break down whats going on here:
1. You’re feeding input into the container as if a user typed it. When Blackbird asks for Y/N?, you want the Y inserted for you automatically
2. So for printf "y\ny\n", each \n means hit the Enter key. Here we do two y's in case it asks for it. 
3. With this: printf "y\ny\n" | docker run ... The pipe sends the output of printf into Docker’s stdin.
4. -i = keep STDIN open. Without it the container ignores input and you get an EOF error
5. If you look inside blackbird.py script there is a section that has this prompt
```
confirm = input(" > ")
```
6. That input() reads from stdin. Because of the pipe, stdin contains: y and y. You can probably remove the second Y if its not needed at all.









