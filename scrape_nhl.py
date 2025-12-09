import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import sys


# --------- SCRAPE NHL GAME LOG FOR A PLAYER ---------
def scrape_player(player_url, player_name, team):
    """Scrape last 3 NHL games (TOI, PP, SOG, G, A, PTS, Opponent, Date)."""

    try:
        response = requests.get(player_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select("table tbody tr")
        game_data = []

        for r in rows[:3]:  # last 3 games
            cols = [c.get_text(strip=True) for c in r.find_all("td")]

            game = {
                "player": player_name,
                "team": team,
                "game_date": cols[0],
                "opponent": cols[1],
                "toi": float(cols[2].replace(":", ".")),  
                "pp_time": float(cols[3].replace(":", ".")),
                "sog": float(cols[4]),
                "goals": float(cols[5]),
                "assists": float(cols[6]),
                "points": float(cols[7]),
            }

            game_data.append(game)

        print(json.dumps(game_data))
        return game_data

    except Exception as e:
        print("ERROR:", e)
        return []



# --------- RENDER ENTRY POINT ---------
if __name__ == "__main__":
    # Player values passed from Render cron job
    player_url = sys.argv[1]
    player_name = sys.argv[2]
    team = sys.argv[3]

    scrape_player(player_url, player_name, team)
