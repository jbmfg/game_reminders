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
        message = f"{dow} @ {gt}"
    pd = {
            "token": token,
            "user": user_key,
            "title": f"{a_a}@{h_a}",
            "message": message,
            "sound": "intermission",
            "ttl": 86400
            }
    push_url = 'https://api.pushover.net/1/messages.json'
    pushover = requests.post(push_url, json=pd)

def get_game_data():
    all_games_url = "https://sportapi.sportingkc.com/api/matches?culture=en-us&dateFrom=2024-12-31&dateTo=2025-12-31&clubOptaId=421"
    all_games_url = "https://sportapi.sportingkc.com/api/matches/bySportecIds/MLS-MAT-0009BD,MLS-MAT-0009BN,MLS-MAT-0009C3,MLS-MAT-0009CI,MLS-MAT-0009CW,MLS-MAT-0009DH,MLS-MAT-0009DR,MLS-MAT-0009E0,MLS-MAT-0009ER,MLS-MAT-0009F9,MLS-MAT-0009FS,MLS-MAT-0009G3,MLS-MAT-0009GD,MLS-MAT-0009GX,MLS-MAT-0009HA,MLS-MAT-0009HJ,MLS-MAT-0009HV,MLS-MAT-0009IC,MLS-MAT-0009IP,MLS-MAT-0009J5,MLS-MAT-0009JT,MLS-MAT-0009K0,MLS-MAT-0009KF,MLS-MAT-0009L1,MLS-MAT-0009L9,MLS-MAT-0009LO,MLS-MAT-0009M3,MLS-MAT-0009MI,MLS-MAT-0009N2,MLS-MAT-0009NA,MLS-MAT-0009NS,MLS-MAT-0009O6,MLS-MAT-0009OJ,MLS-MAT-0009P7"
    r = requests.get(all_games_url)
    if r.status_code == 200:
        data = r.json()
        data = sorted(data, key=lambda x: x["matchDate"])

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
    md = md - timedelta(hours=4)
    return home, h_a, away, a_a, md, days_to_go

if __name__ == "__main__":
    home, h_a, away, a_a, md, days_to_go = get_game_data()
    push_game(home, h_a, away, a_a, md, days_to_go)



