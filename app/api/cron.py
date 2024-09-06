from app.scrap.hltv import get_upcoming_matches, save_matches_to_json

def cron_job(req, res):
    print("Updating Brazilian matches...")
    matches = get_upcoming_matches()
    save_matches_to_json(matches)
    print("Updated matches!")
    
    return res.status(200).json({"message": "Matches updated successfully!"})
