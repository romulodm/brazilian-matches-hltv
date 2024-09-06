from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

brazilian_teams = [
    "paiN", "FURIA", "MIBR", "Imperial", "ODDIK", "Legacy", "RED Canids",
    "Fluxo", "Case", "Sharks", "InSanity", "E-xolos LAZER", "Solid", "Hype", "Bounty Hunters"
]

def get_upcoming_matches():
    url = "https://www.hltv.org/matches"
    
    # Browser settings
    options = Options()
    options.headless = True  # Run the browser in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # May be required in some configurations
    options.add_argument('--disable-software-rasterizer')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url) # Making the request
    time.sleep(2) # Waiting for loading
    
    html = driver.page_source # Getting the page's html
    soup = BeautifulSoup(html, 'html.parser')

    matches = []

    for match in soup.select('.upcomingMatch'):
        team_1_element = match.select_one('.matchTeam.team1 .matchTeamName')
        team_2_element = match.select_one('.matchTeam.team2 .matchTeamName')
        match_time_element = match.select_one('.matchTime')
        match_event_element = match.select_one('.matchEvent')
        match_link_element = match.select_one('.match.a-reset')

        # Checking if elements exist before accessing their properties
        if team_1_element and team_2_element and match_time_element and match_event_element and match_link_element:
            team_1 = team_1_element.text.strip()
            team_2 = team_2_element.text.strip() 
            match_time = match_time_element.text.strip()

            date = match_time_element.get('data-unix')
            
            # Team images
            team_1_logo_element = match.select_one('.matchTeam.team1 .matchTeamLogo')
            team_2_logo_element = match.select_one('.matchTeam.team2 .matchTeamLogo')
            
            team_1_logo = team_1_logo_element['src'] if team_1_logo_element and 'src' in team_1_logo_element.attrs else "N/A"
            team_2_logo = team_2_logo_element['src'] if team_2_logo_element and 'src' in team_2_logo_element.attrs else "N/A"

            # Event information
            event_name_element = match_event_element.select_one('.matchEventName')
            event_logo_element = match_event_element.select_one('.matchEventLogo')
            
            event_name = event_name_element.text.strip() if event_name_element else "N/A"
            event_logo = event_logo_element['src'] if event_logo_element and 'src' in event_logo_element.attrs else "N/A"

            # Link to HLTV's match page
            match_link = "https://www.hltv.org" + match_link_element['href']

            if date and (team_1 in brazilian_teams or team_2 in brazilian_teams):
                match_info = {
                    "team_1": team_1,
                    "team_1_logo": team_1_logo,
                    "team_2": team_2,
                    "team_2_logo": team_2_logo,
                    "time": match_time,
                    "date": datetime.fromtimestamp(int(date)/1000).strftime('%Y-%m-%d %H:%M:%S'),
                    "event_name": event_name,
                    "event_logo": event_logo,
                    "match_link": match_link
                }
                matches.append(match_info)

    driver.quit() # Closing navigator
    return matches

def save_matches_to_json(matches):
    with open('brazilian_matches.json', 'w') as json_file:
        json.dump(matches, json_file, indent=4)