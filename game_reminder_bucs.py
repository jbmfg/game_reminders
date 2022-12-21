import datetime
import requests
import json


today = datetime.datetime.now()

with open("/home/jbg/dev/sports_reminders/pushover_settings.conf", "r") as f:
    settings = json.load(f)
token, user_key = settings["bucs"], settings["user_key"]

with open("/home/jbg/dev/sports_reminders/2022_bucs_schedule.ics", "r") as f:
    data = f.read()
    game_data = data.split("BEGIN:VEVENT")
    for game in game_data[1:]:
        game_details = game.split("\n")
        #for x,i in enumerate(game_details): print(f"{x} - {i}")
        for x, i in enumerate(game_details):
            if "DTSTART" in i:
                date_part = game_details[x].split(":")[1]
                if len(date_part) == 8:
                    format = "%Y%m%d"
                else:
                    format = "%Y%m%dT%H%M%SZ"
                game_datetime = datetime.datetime.strptime(date_part, format)
                if len(date_part) !=8:
                    game_datetime -= datetime.timedelta(hours=4)
        if game_datetime >= today:
            relative_gd =\
            "Today!" if game_datetime.date() == today.date() else f"In {(game_datetime.date()-today.date()).days} days"
            for x, i in enumerate(game_details):
                if "SUMMARY" in i:
                    if "at Tampa Bay Buccaneers" in i:
                        home_away = "home"
                    else:
                        home_away = "away"
                    opponent = game_details[x].split(":")[1]
                    opponent = opponent.replace("Tampa Bay Buccaneers", "").replace("at", "").strip()
                    opponent = f"{opponent} ({home_away})"
                if "Watch the game on" in i:
                    tv = game_details[x].split(r"--")[1].replace("Watch the game on ", "").replace("\\n","")
            break

    pd = {
            "token": token,
            "user": user_key,
            "title": f"TB Bucs vs {opponent} {relative_gd}",
            "message": f"{tv} @ {game_datetime}",
            "sound": "intermission"
            }
    push_url = 'https://api.pushover.net/1/messages.json'
    pushover = requests.post(push_url, json=pd)



