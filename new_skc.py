import json
import requests
from datetime import datetime, timedelta

def push_game(home, h_a, away, a_a, md, days_to_go):
    with open("/home/jbg/game_reminders/pushover_settings.conf", "r") as f:
        settings = json.load(f)
    token, user_key = settings["skc"], settings["user_key"]
    if days_to_go >= 7:
        message = f"Game in {days_to_go} days"
    else:
        dow = datetime.strftime(md, "%A")
        gt = datetime.strftime(md, "%I:%M %p")
        message = f"Game on {dow} @ {gt}"
    pd = {
            "token": token,
            "user": user_key,
            "title": f"{a_a}@{h_a}",
            "message": message,
            "sound": "intermission"
            }
    push_url = 'https://api.pushover.net/1/messages.json'
    pushover = requests.post(push_url, json=pd)

def get_game_data():
    all_games_url = "https://sportapi.sportingkc.com/api/matches?culture=en-us&dateFrom=2023-12-31&dateTo=2024-12-31&clubOptaId=421"
    r = requests.get(all_games_url)
    if r.status_code == 200:
        data = r.json()

        now = datetime.utcnow()
        fmt = "%Y-%m-%dT%H:%M:%S.0000000Z"
        for game in data:
            home = game["home"]["fullName"]
            h_a = game["home"]["abbreviation"]
            away = game["away"]["fullName"]
            a_a = game["away"]["abbreviation"]
            match_date = game["matchDate"]
            md = datetime.strptime(match_date, fmt)
            if md > now:
                break
    days_to_go = (md - now).days
    md = md - timedelta(hours=5)
    return home, h_a, away, a_a, md, days_to_go

if __name__ == "__main__":
    home, h_a, away, a_a, md, days_to_go = get_game_data()
    push_game(home, h_a, away, a_a, md, days_to_go)



