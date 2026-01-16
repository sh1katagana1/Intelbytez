# Robin Dark Web AI Search

***

## Description
Robin is an AI-powered tool for conducting dark web OSINT investigations. It leverages LLMs to refine queries, filter search results from dark web search engines, and provide an investigation summary.

## Link
https://github.com/apurvsinghgautam/robin

## Example
![](https://github.com/apurvsinghgautam/robin/raw/main/.github/assets/screen.png)

## Features
1. Modular Architecture – Clean separation between search, scrape, and LLM workflows.
2. Multi-Model Support – Easily switch between OpenAI, Claude, Gemini or local models like Ollama.
3. CLI-First Design – Built for terminal warriors and automation ninjas.
4. Docker-Ready – Optional Docker deployment for clean, isolated usage.
5. Custom Reporting – Save investigation output to file for reporting or further analysis.
6. Extensible – Easy to plug in new search engines, models, or output formats.

## Prerequisites
The tool needs Tor to do the searches. You can install Tor using 
```
apt install tor
```
You can provide OpenAI or Anthropic or Google API key by either creating .env file (refer to sample env file in the repo) or by setting env variables in PATH.

## Install (Docker)
I chose to use Docker to run this. 
```
docker pull apurvsg/robin:latest
```
As you have to pay for an OpenAI API Key, I already had a Gemini one so I just used that. I noticed that by default it seems to look for an OpenAI API key, so I told it to disregard it
```
docker run --rm \
  -e GOOGLE_API_KEY="GEMINI API KEY" \
  -e OPENAI_API_KEY="sk-not-used" \
  --add-host=host.docker.internal:host-gateway \
  -p 8501:8501 \
  apurvsg/robin:latest ui --ui-port 8501 --ui-host 0.0.0.0
```
This ran and created a webpage on http://0.0.0.0:8501. When you browse to it, there is a Model dropdown box on the left, select the Gemini Flash model.

## Usage
With the GUI its pretty straight forward, it gives you a search box, type in your search and hit enter. When its done, it will display all relevant data and links and have a downloadable PDF. 

For CLI:
```
Robin: AI-Powered Dark Web OSINT Tool

options:
  -h, --help            show this help message and exit
  --model {gpt4o,gpt-4.1,claude-3-5-sonnet-latest,llama3.1,gemini-2.5-flash}, -m {gpt4o,gpt-4.1,claude-3-5-sonnet-latest,llama3.1,gemini-2.5-flash}
                        Select LLM model (e.g., gpt4o, claude sonnet 3.5, ollama models, gemini 2.5 flash)
  --query QUERY, -q QUERY
                        Dark web search query
  --threads THREADS, -t THREADS
                        Number of threads to use for scraping (Default: 5)
  --output OUTPUT, -o OUTPUT
                        Filename to save the final intelligence summary. If not provided, a filename based on the
                        current date and time is used.

Example commands:
 - robin -m gpt4.1 -q "ransomware payments" -t 12
 - robin --model gpt4.1 --query "sensitive credentials exposure" --threads 8 --output filename
 - robin -m llama3.1 -q "zero days"
 - robin -m gemini-2.5-flash -q "zero days"
```
























