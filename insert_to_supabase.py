import sys
import json
from supabase import create_client, Client
from datetime import datetime
import os


# --------- CONNECT TO SUPABASE ---------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --------- INSERT SCRAPED DATA INTO SUPABASE ---------
def insert_logs(json_data):
    try:
        logs = json.loads(json_data)

        for g in logs:
            supabase.table("nhl_player_logs").insert({
                "player": g["player"],
                "team": g["team"],
                "game_date": g["game_date"],
                "opponent": g["opponent"],
                "toi": g["toi"],
                "pp_time": g["pp_time"],
                "sog": g["sog"],
                "goals": g["goals"],
                "assists": g["assists"],
                "points": g["points"],
                "line_assignment": None,
                "pp_unit": None
            }).execute()

        print("SUCCESS: Logs inserted.")

    except Exception as e:
        print("ERROR inserting logs:", e)


# --------- ENTRY POINT (Render Pipe) ---------
if __name__ == "__main__":
    raw = sys.argv[1]  # JSON from scrape_nhl.py
    insert_logs(raw)
