from app.scrap.hltv import *

def main():
    matches = get_upcoming_matches()
    save_matches_to_json(matches)
    print(f"{len(matches)} partidas salvas com sucesso!")

if __name__ == "__main__":
    main()