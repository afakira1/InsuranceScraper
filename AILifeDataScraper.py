#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AILife Insurance Web Scraper and Database Generator

Purpose: The purpose of this program is to automate the collection and database
generation of AILife Insurance company agent information. This database can be used 
for EDA, forecast modeling, etc.

@author: amerfakira
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import re

state_dict = {
    'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',
    'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','Florida': 'FL','Georgia': 'GA',
    'Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA',
    'Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD',
    'Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS',
    'Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH',
    'New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC',
    'North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR',
    'Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC',
    'South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT',
    'Vermont': 'VT','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV',
    'Wisconsin': 'WI','Wyoming': 'WY'
}

def extract_state(address):
    for full_name, abbrev in state_dict.items():
        if full_name in address:
            return abbrev
    state_match = re.search(r'\b[A-Z]{2}\b', address)
    return state_match.group() if state_match else "State not found"

def scrape_agents():

    all_agent_data = []
    base_url = 'https://agency.ailife.com'

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    us_link = soup.find('a', string='United States')
    us_url = us_link['href']

    response = requests.get(us_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    state_links_container = soup.find('div', class_='search-bottom__results')

    for state_link in state_links_container.find_all('a'):
        state_url = state_link['href']

        if state_url.startswith('/united-states/'):
            state_url = f"{base_url}{state_url}"

            state_response = requests.get(state_url)
            state_soup = BeautifulSoup(state_response.content, 'html.parser')
            city_links_container = state_soup.find('div', class_='search-bottom__results')

            if city_links_container:
                for city_entry in city_links_container.find_all('div', class_='search-bottom__entry'):
                    city_link = city_entry.find('a')
                    if city_link and city_link['href'].startswith('/united-states/'):
                        city_url = f"{base_url}{city_link['href']}"

                        city_response = requests.get(city_url)
                        city_soup = BeautifulSoup(city_response.content, 'html.parser')
                        agent_list_results = city_soup.find('div', class_='agent-list-results')

                        if agent_list_results:
                            for agent_card in agent_list_results.find_all('div', class_='agent-card'):
                                agent_name_full = agent_card.find('span', class_='agent-card-name').text.strip()

                                agent_addy1 = ' '.join([a.text.strip() for a in agent_card.find_all('span', class_='agent-card-addy1')])
                                agent_addy2 = agent_card.find('span', class_='agent-card-addy2').text.strip()
                                agent_phone = agent_card.find('span', class_='agent-card-phone').text.strip()

                                agent_website_element = agent_card.find('span', class_='agent-card-locationurl').find('a')
                                agent_website = agent_website_element['href'] if agent_website_element else ""

                                agent_address = f"{agent_addy1} {agent_addy2}".strip()
                                state = extract_state(agent_address)

                                names = re.split(r'\s*&\s*|\s*,\s*', agent_name_full)

                                for name in names:
                                    all_agent_data.append({
                                        'Individual Agents': name.strip(),
                                        'Name On Site': agent_name_full,
                                        'Address': agent_address,
                                        'State': state,
                                        'Phone': agent_phone,
                                        'Website': f"{base_url}{agent_website}"
                                    })

                        time.sleep(1)

    df_agents = pd.DataFrame(all_agent_data)

    agent_offices = defaultdict(set)
    for _, row in df_agents.iterrows():
        agent_offices[row['Individual Agents']].add(row['Address'])

    df_agents['# Of Offices'] = df_agents['Individual Agents'].apply(lambda x: len(agent_offices[x]))

    df_agents = df_agents.sort_values(by=['# Of Offices', 'Individual Agents'], ascending=[False, True])

    df_agents.to_excel("AILife_Agents_Data.xlsx", index=False)

    return df_agents

if __name__ == '__main__':
    scrape_agents()