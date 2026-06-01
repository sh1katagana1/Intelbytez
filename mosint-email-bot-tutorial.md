# MOSINT OSINT Email Bot

***

## Goals
I want to use MOSINT https://github.com/alpkeskin/mosint as the source for a Telegram bot, wherein I give an email address and it enriches it and gives me an HTML report on it with risk scoring. I choose MOSINT because normally my main sources of email OSINT are Emailrep.io, Hunter.io and HaveIBeenPwned. MOSINT uses all 3 and does output to JSON which can be utilized by my bot for a nice report.

## Workflow Diagram
```
[1] MOSINT (Docker)
        ↓
[2] JSON output (raw intelligence)
        ↓
[3] render.py (processing + risk scoring)
        ↓
[4] report.html (final human-readable OSINT report)
```

## Folder Structure
```
docker-stuff/
│
├── mosint/
│   ├── output/
│   │   ├── result.json      ← MOSINT output (input to your system)
│   │   └── report.html      ← FINAL generated report
│
├── templates/
│   └── report.html         ← HTML layout (Jinja template)
│
├── render.py               ← CORE processing script
├── bot.py                  ← (not built yet)
├── venv/
```

I made a Python virtual environment to install the PIP package Jinja2, which is used for the HTML generation
```
pip3 install jinja2
```
The render.py script is what will be run locally to test this before making it a Telegram Bot. The Templates folder has report.html, which Jinja2 will use as its HTML template base. The MOSINT folder has a folder I made called output that will contain the JSON file it generates. MOSINT is being run in Docker. How I did this is I cloned the MOSINT repo:
```
git clone https://github.com/alpkeskin/mosint
```
It has a Dockerfile already, so I built it 
```
docker build -t mosint .
```
MOSINT has an example-config.yaml that it uses for me to provide the API Keys for emailrep, hunter and hibp. However its not wise to have these baked into the image, so I chose to make a custom one based off of that example file, called my-config.yaml, and it will be injected at runtime. My initial run to test it, where it only spins up the container and then deletes it after giving the results is:
```
docker run --rm \
  -v $(pwd)/my-config.yaml:/root/.mosint.yaml \
  mosint \
  acidicloop@gmail.com
```
The pwd/my-config.yaml part is doing something called a mount, where I am passing in the config file. To test the JSON output, I run:
```
docker run --rm \
  -v $(pwd)/my-config.yaml:/root/.mosint.yaml \
  -v $(pwd)/output:/output \
  mosint \
  -o /output/result.json \
  acidicloop@gmail.com
```
The first -v section is to pass in the config file. The second one is saying where to pass the JSON file results locally. That is because when the container runs, it gets the results, generates the json file and puts it in a folder called output inside of MOSINT folder. However, because we have this deleting the container after it runs, that file is also removed. To have it pass it to my local MOSINT output folder, I need to mount that folder. Now when the container runs, it generates the file locally in my MOSINT folder, so that I do have that file even after the container is deleted. 

So that is the current way that MOSINT will be run, but we want the JSON parsed and the results risk scored and made into a nice HTML output. In this case, MOSINT is just the data collector, not the formatter or interpreter.

## Render.py 
This will be my core logic for this. 
```
import json
import os
from jinja2 import Template

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_PATH = os.path.join(BASE_DIR, "mosint", "output", "result.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "report.html")
OUTPUT_PATH = os.path.join(BASE_DIR, "mosint", "output", "report.html")


# ----------------------------
# Load JSON
# ----------------------------
with open(JSON_PATH, "r") as f:
    data = json.load(f)


# ----------------------------
# Safe helpers
# ----------------------------
def safe_dict(obj):
    return obj if isinstance(obj, dict) else {}

def safe_list(obj):
    return obj if isinstance(obj, list) else []


# ----------------------------
# Risk scoring function
# ----------------------------
def calculate_risk(data):
    score = 0

    emailrep = safe_dict(data.get("emailrep"))
    details = safe_dict(emailrep.get("details"))

    # Reputation
    if emailrep.get("reputation") != "high":
        score += 30

    # Leak signals
    if details.get("credentials_leaked"):
        score += 40

    if details.get("data_breach"):
        score += 20

    if details.get("malicious_activity"):
        score += 30

    if details.get("malicious_activity_recent"):
        score += 40

    # Abuse signals
    if details.get("spam"):
        score += 10

    if details.get("blacklisted"):
        score += 50

    # Domain risk signals
    if details.get("disposable"):
        score += 50

    if details.get("spoofable"):
        score += 15

    return min(score, 100)


# ----------------------------
# Core fields
# ----------------------------
email = data.get("email", "unknown")
haveibeenpwned = safe_list(data.get("haveibeenpwned"))
dns_records = safe_list(data.get("dns_records"))

emailrep = safe_dict(data.get("emailrep"))
hunter = safe_dict(data.get("hunter"))

# ----------------------------
# Risk score
# ----------------------------
risk_score = calculate_risk(data)

# ----------------------------
# Load template
# ----------------------------
with open(TEMPLATE_PATH, "r") as f:
    template = Template(f.read())

# ----------------------------
# Render HTML
# ----------------------------
html = template.render(
    email=email,
    haveibeenpwned=haveibeenpwned,
    emailrep=emailrep,
    hunter=hunter,
    dns_records=dns_records,
    risk_score=risk_score
)

# ----------------------------
# Save output
# ----------------------------
with open(OUTPUT_PATH, "w") as f:
    f.write(html)

print(f"[+] Report generated: {OUTPUT_PATH}")
print(f"[+] Risk Score: {risk_score}/100")
```

Let's breakdown this script in sections:

### Imports
```
import json
import os
from jinja2 import Template
```
1. json - reads MOSINT output
2. os - handles file paths safely
3. jinja2 - fills HTML template with data

### File Paths
```
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JSON_PATH = os.path.join(BASE_DIR, "mosint", "output", "result.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "report.html")
OUTPUT_PATH = os.path.join(BASE_DIR, "mosint", "output", "report.html")
```
Defines where everything is:
1. input JSON (MOSINT output)
2. HTML template
3. output report

### Load MOSINT Data
```
with open(JSON_PATH, "r") as f:
    data = json.load(f)
```
This opens result.json and converts JSON to a Python dictionary. Now the 'data' variable will look like:
```
{
  "email": "...",
  "emailrep": {...},
  "haveibeenpwned": [...]
}
```

### Helper Functions
```
def safe_dict(obj):
    return obj if isinstance(obj, dict) else {}

def safe_list(obj):
    return obj if isinstance(obj, list) else []
```
MOSINT APIs sometimes return:
1. null
2. missing fields
3. broken objects

So this prevents crashes.

### Risk Scoring Engine
```
def calculate_risk(data):
```
Turns raw OSINT into a score from 0–100. 
```
score = 0
``` 
Starts them with no risk score. 

```
if emailrep.get("reputation") != "high":
    score += 30
```
Bad reputation = risk increases

```
if credentials_leaked:
    score += 40

if data_breach:
    score += 20
```
If email is in leaks this equals high risk.

```
malicious_activity → +30
recent activity → +40
blacklisted → +50
```
These are strong red flags

```
disposable → +50
spoofable → +15
```
Fake/temp emails = very risky

```
return min(score, 100)
```
A clamp to prevent scores going above 100.

### Extracting Data Safely
```
email = data.get("email")
haveibeenpwned = safe_list(data.get("haveibeenpwned"))
dns_records = safe_list(data.get("dns_records"))
emailrep = safe_dict(data.get("emailrep"))
hunter = safe_dict(data.get("hunter"))
```
Extracts each OSINT source safely.

### Risk calculation call
```
risk_score = calculate_risk(data)
```
This generates the final score.

### Load HTML Template
```
template = Template(f.read())
```
Loads your HTML file as a Jinja template.

### Renders Final HTML
```
html = template.render(
    email=email,
    haveibeenpwned=haveibeenpwned,
    emailrep=emailrep,
    hunter=hunter,
    dns_records=dns_records,
    risk_score=risk_score
)
```
Injects Python data into HTML like:
```
{{ email }}
{{ risk_score }}
```

### Save Output
```
with open(OUTPUT_PATH, "w") as f:
    f.write(html)
```
Writes final report file

### Print Status
```
print(f"[+] Risk Score: {risk_score}/100")
```
Just feedback for you.


## Report.html
```
<html>
<head>
  <style>
    body {
      font-family: Arial;
      background: #0b1220;
      color: #e5e7eb;
      padding: 20px;
    }

    h1 {
      color: #38bdf8;
    }

    .card {
      background: #111827;
      padding: 15px;
      margin: 10px 0;
      border-radius: 10px;
      border: 1px solid #1f2937;
    }

    .good { color: #34d399; }
    .bad { color: #fb7185; }
    .muted { color: #9ca3af; }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    td {
      padding: 6px;
      border-bottom: 1px solid #1f2937;
    }
  </style>
</head>

<body>

<h1>OSINT Report</h1>
<p class="muted">Target: {{ email }}</p>

<!-- ===================== -->
<!-- RISK SCORE -->
<!-- ===================== -->
<div class="card">
  <h2>Risk Score</h2>

  {% if risk_score >= 70 %}
    <p class="bad">🔴 HIGH RISK ({{ risk_score }}/100)</p>
  {% elif risk_score >= 40 %}
    <p style="color:#fbbf24">🟡 MEDIUM RISK ({{ risk_score }}/100)</p>
  {% else %}
    <p class="good">🟢 LOW RISK ({{ risk_score }}/100)</p>
  {% endif %}

  <p class="muted">Calculated from breaches, reputation, and abuse signals</p>
</div>

<!-- ===================== -->
<!-- HAVE I BEEN PWNED -->
<!-- ===================== -->
<div class="card">
  <h2>HaveIBeenPwned Breaches</h2>

  {% if haveibeenpwned and haveibeenpwned|length > 0 %}
    {% for b in haveibeenpwned %}
      <p class="bad">
        🔴 {{ b.Name }} ({{ b.BreachDate }}) — {{ b.PwnCount }} accounts
      </p>
      <p class="muted">{{ b.Description | safe }}</p>
    {% endfor %}
  {% else %}
    <p class="good">✅ No breaches found</p>
  {% endif %}
</div>

<!-- ===================== -->
<!-- EMAIL REP -->
<!-- ===================== -->
<div class="card">
  <h2>Email Reputation</h2>

  {% if emailrep %}
    <p>Reputation:
      {% if emailrep.reputation == "high" %}
        <span class="good">{{ emailrep.reputation }}</span>
      {% elif emailrep.reputation == "medium" %}
        <span style="color:#fbbf24">{{ emailrep.reputation }}</span>
      {% else %}
        <span class="bad">{{ emailrep.reputation }}</span>
      {% endif %}
    </p>

    <p>Credentials leaked: {{ emailrep.details.credentials_leaked }}</p>
    <p>Data breach: {{ emailrep.details.data_breach }}</p>
    <p>Deliverable: {{ emailrep.details.deliverable }}</p>
    <p>Disposable: {{ emailrep.details.disposable }}</p>
    <p>Spam risk: {{ emailrep.details.spam }}</p>
  {% else %}
    <p class="muted">No EmailRep data available</p>
  {% endif %}
</div>

<!-- ===================== -->
<!-- HUNTER -->
<!-- ===================== -->
<div class="card">
  <h2>Hunter Domain Intelligence</h2>

  {% if hunter and hunter.data %}
    <p>Domain: {{ hunter.data.domain }}</p>
    <p>Webmail: {{ hunter.data.webmail }}</p>
    <p>Disposable: {{ hunter.data.disposable }}</p>
    <p>Accept all: {{ hunter.data.accept_all }}</p>
    <p>Organization: {{ hunter.data.organization }}</p>
  {% else %}
    <p class="muted">No Hunter data available</p>
  {% endif %}
</div>

<!-- ===================== -->
<!-- DNS -->
<!-- ===================== -->
<div class="card">
  <h2>DNS Records</h2>

  {% if dns_records and dns_records|length > 0 %}
    <table>
      {% for r in dns_records %}
        <tr>
          <td class="muted">{{ r.Type }}</td>
          <td>{{ r.Value }}</td>
        </tr>
      {% endfor %}
    </table>
  {% else %}
    <p class="muted">No DNS records found</p>
  {% endif %}
</div>

</body>
</html>
```
This is your presentation layer. It:
1. displays email
2. shows breaches
3. shows EmailRep data
4. shows Hunter data
5. shows DNS records
6. shows risk score visually


## Summary
Here is your full pipeline in simple terms:

* Step 1 - You input email
* Step 2 - MOSINT gathers raw intelligence
* Step 3 - render.py:
```
cleans data
calculates risk
organizes structure
```
* Step 4 - HTML file shows everything in readable format

























































 
