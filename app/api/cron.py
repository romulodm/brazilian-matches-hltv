from flask import jsonify
from app.scrap.hltv import get_upcoming_matches, save_matches_to_json

def cron_job():
    print("Updating Brazilian matches...")
    matches = get_upcoming_matches()
    save_matches_to_json(matches)
    print("Updated matches!")
    
    return jsonify({"message": "Matches updated successfully!"}), 200
