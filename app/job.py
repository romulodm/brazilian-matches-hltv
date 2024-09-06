import schedule
import time
from app.scrap.hltv import get_upcoming_matches, save_matches_to_json

def job():
    print("Updating Brazilian matches...")
    matches = get_upcoming_matches()  # Função do scraping
    save_matches_to_json(matches)
    print("Updated matches!")

def run_schedule():
    # Schedule the function to run every day at 06:00
    schedule.every().day.at("06:00").do(job)

    # Loop to keep the schedule running
    while True:
        schedule.run_pending()
        time.sleep(600)
