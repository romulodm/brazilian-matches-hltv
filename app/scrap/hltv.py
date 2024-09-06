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
    
    # Configurações do navegador
    options = Options()
    options.headless = True  # Executa o navegador em modo headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Pode ser necessário em algumas configurações
    options.add_argument('--disable-software-rasterizer')

    # Inicializa o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Faz a requisição para a página
    driver.get(url)
    
    # Aguarda alguns segundos para garantir que a página carregou
    time.sleep(2)
    
    # Obtém o HTML da página
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Lista de partidas
    matches = []

    # Loop em todas as partidas
    for match in soup.select('.upcomingMatch'):
        team_1_element = match.select_one('.matchTeam.team1 .matchTeamName')
        team_2_element = match.select_one('.matchTeam.team2 .matchTeamName')
        match_time_element = match.select_one('.matchTime')

        # Verifica se os elementos existem antes de acessar suas propriedades
        if team_1_element and team_2_element and match_time_element:
            team_1 = team_1_element.text.strip()
            team_2 = team_2_element.text.strip()
            match_time = match_time_element.text.strip()
            date = match_time_element.get('data-unix')

            if date and (team_1 in brazilian_teams or team_2 in brazilian_teams):
                match_info = {
                    "team_1": team_1,
                    "team_2": team_2,
                    "time": match_time,
                    "date": datetime.fromtimestamp(int(date)/1000).strftime('%Y-%m-%d %H:%M:%S')
                }
                matches.append(match_info)

    driver.quit()  # Fecha o navegador
    return matches

def save_matches_to_json(matches):
    with open('brazilian_matches.json', 'w') as json_file:
        json.dump(matches, json_file, indent=4)
