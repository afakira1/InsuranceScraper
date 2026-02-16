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

#### Step 4. Extract Agent Information

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
