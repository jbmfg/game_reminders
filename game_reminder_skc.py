import datetime
import json
import requests
import pytz
from calendar import day_abbr


today = datetime.datetime.now()

with open("/home/jbg/dev/sports_reminders/pushover_settings.conf", "r") as f:
    settings = json.load(f)
token, user_key = settings["skc"], settings["user_key"]

with open("/home/jbg/dev/sports_reminders/2023_sportingkc_schedule.ics", "r") as f:
    data = f.read()
    game_data = data.split("BEGIN:VEVENT")
    for game in game_data[1:]:
        game_details = game.split("\n")
        game_datetime = datetime.datetime.strptime(game_details[1].split(":")[1], "%Y%m%dT%H%M%SZ") - datetime.timedelta(hours=4)
        est = pytz.timezone("US/Eastern")
        game_datetime_est = game_datetime.astimezone(est)
        weekday = day_abbr[game_datetime_est.weekday()]
        game_datetime_est = datetime.datetime.strftime(game_datetime_est, "%h %d @ %I:%M %p")
        if game_datetime >= today:
            else_txt = f"In {(game_datetime.date()-today.date()).days} days"
            relative_gd = "Today!" if game_datetime.date() == today.date() else else_txt
            opponent = game_details[4].split(":")[1].replace("Sporting Kansas City", "").strip()
            tv = game_details[5].split(r"\n")[0].replace("DESCRIPTION:Watch:", "").replace("MLS LIVE on DAZN", "").split(",")
            tv = ", ".join([i.strip() for i in tv if len(i) > 1])
            break

    pd = {
            "token": token,
            "user": user_key,
            "title": f"SKC {opponent} {relative_gd}",
            "message": f"{weekday} {game_datetime_est} on {tv}",
            "sound": "intermission"
            }
    push_url = 'https://api.pushover.net/1/messages.json'
    pushover = requests.post(push_url, json=pd)



