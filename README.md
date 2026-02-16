# Agent Data Extraction from AILife Directory

## Description

The aim of this project is to create a structured dataset of insurance agents by scraping the public directory located at:

https://agency.ailife.com

The final dataset contains:

- Individual Agent Name  
- Name as Listed on Site  
- Office Address  
- State  
- Phone Number  
- Website  
- Number of Offices per Agent  

---

## Python Libraries and Utilities

- Requests  
- BeautifulSoup  
- Pandas  
- Regex  
- Collections  

---

## Project Walk-through

### Setup

#### Step 1. Load Libraries

```python
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
```
---

### Data Normalization

#### Step 2. Extract State from Address

This function standardizes location data by extracting the agent's state from their office address.

```python
def extract_state(address):
    for full_name, abbrev in state_dict.items():
        if full_name in address:
            return abbrev
    state_match = re.search(r'\b[A-Z]{2}\b', address)
    return state_match.group() if state_match else "State not found"
```
---

### Scraping Workflow

#### Step 3. Navigate from Country → State → City

The scraper begins at the homepage, locates the **United States directory**, and then iterates through:

- All state pages  
- All city pages within each state

```python
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
us_link = soup.find('a', string='United States')
```
---
#### Step 4. Full Crawling + Agent Extraction

> **Note:** The expandable block below contains the full end-to-end scraping loop.
> The steps that follow highlight the key parts of the workflow with short, readable snippets.
<details>
<summary><b>View scraping loop</b></summary>

```python
all_agent_data = []
base_url = "https://agency.ailife.com"

response = requests.get(base_url)
soup = BeautifulSoup(response.content, "html.parser")

us_link = soup.find("a", string="United States")
if not us_link:
    raise RuntimeError("Could not find 'United States' link.")

us_url = us_link["href"]

response = requests.get(us_url)
soup = BeautifulSoup(response.content, "html.parser")

state_links_container = soup.find("div", class_="search-bottom__results")
if not state_links_container:
    raise RuntimeError("Could not find state links container.")

for state_link in state_links_container.find_all("a"):
    state_href = state_link.get("href", "")
    if not state_href.startswith("/united-states/"):
        continue

    state_url = f"{base_url}{state_href}"

    state_response = requests.get(state_url)
    state_soup = BeautifulSoup(state_response.content, "html.parser")

    city_links_container = state_soup.find("div", class_="search-bottom__results")
    if not city_links_container:
        continue

    for city_entry in city_links_container.find_all("div", class_="search-bottom__entry"):
        city_anchor = city_entry.find("a")
        if not city_anchor:
            continue

        city_href = city_anchor.get("href", "")
        if not city_href.startswith("/united-states/"):
            continue

        city_url = f"{base_url}{city_href}"

        city_response = requests.get(city_url)
        city_soup = BeautifulSoup(city_response.content, "html.parser")

        agent_list_results = city_soup.find("div", class_="agent-list-results")
        if not agent_list_results:
            continue

        for agent_card in agent_list_results.find_all("div", class_="agent-card"):
            name_el = agent_card.find("span", class_="agent-card-name")
            agent_name_full = name_el.text.strip() if name_el else "Name not available"

            addy1_els = agent_card.find_all("span", class_="agent-card-addy1")
            agent_addy1 = " ".join([a.text.strip() for a in addy1_els]) if addy1_els else ""

            addy2_el = agent_card.find("span", class_="agent-card-addy2")
            agent_addy2 = addy2_el.text.strip() if addy2_el else ""

            agent_address = f"{agent_addy1} {agent_addy2}".strip()
            state = extract_state(agent_address)

            phone_el = agent_card.find("span", class_="agent-card-phone")
            agent_phone = phone_el.text.strip() if phone_el else "Phone not available"

            website_url = "Website not available"
            website_container = agent_card.find("span", class_="agent-card-locationurl")
            if website_container:
                a = website_container.find("a")
                if a and a.get("href"):
                    website_url = f"{base_url}{a['href']}"

            names = re.split(r"\s*&\s*|\s*,\s*", agent_name_full)
            for name in names:
                name = name.strip()
                if not name:
                    continue

                all_agent_data.append({
                    "Individual Agents": name,
                    "Name On Site": agent_name_full,
                    "Address": agent_address,
                    "State": state,
                    "Phone": agent_phone,
                    "Website": website_url
                })

        time.sleep(1)
```
</details>

#### Step 4A. Extract Agent Information

For each city page, agent profile cards are parsed to retrieve:

- Agent Name(s)  
- Office Address  
- Phone  
- Website  

Multi-agent listings are split into individual agents for row-level analysis.

```python
agent_list_results = city_soup.find('div', class_='agent-list-results')
```
---

### Data Transformation

#### Step 5. Count Unique Offices per Agent

Each agent’s office count is calculated by tracking unique addresses.

```python
agent_offices = defaultdict(set)
for _, row in df_agents.iterrows():
    agent_offices[row['Individual Agents']].add(row['Address'])
```
---

#### Step 6. Sort Agents by Office Count

Agents are ranked by total number of offices.

```python
df_agents = df_agents.sort_values(by=['# Of Offices', 'Individual Agents'], ascending=[False, True])
```
---

### Output

#### Step 7. Export to Excel

The final dataset is exported into:

"YOUR FILE NAME HERE"

```python
df_agents.to_excel("'YOUR FILE NAME HERE'.xlsx", index=False)
```
---

### Execution
```python
if __name__ == '__main__':
    scrape_agents()
```
<!--
# Insurance Agent Information: Dataset Generation With Scraping

## Description
The aim of this project is to create a data set with information about insurance agents at American Life Insurance Company. The final data set will contain information regarding the:
  - Agent Name
  - The Number of offices they have in the United States
  - Each office's address
  - Each office's phone number

## Python Libraries & Utilities
  - Pandas
  - Beautiful Soup

## Project walk-through:
**Set Up**
** Step 1: **
```python 
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
from datetime import datetime
import re
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
```
-->
