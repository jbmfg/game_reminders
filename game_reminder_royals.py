import csv
import datetime
import requests
import json
import re

with open("/home/jbg/dev/sports_reminders/pushover_settings.conf", "r") as f:
    settings = json.load(f)
token, user_key, youtube = settings["royals"], settings["user_key"], settings["youtube"]

url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PLL-lmlkrmJanUePyXyLusrJGzyGRg-Qj3&maxResults=50&key={youtube}"
headers = {"Authorization": f"Bearer {youtube}"}

r = requests.get(url)
games = r.json()["items"]
highlights = []

for game in games:
    title = game["snippet"]["title"]
    if "Royals" in title:
        date = re.match(r'.+\((\d+\/\d+\/\d+)\)', title).group(1)
        link = f"https://www.youtube.com/watch?v={game['snippet']['resourceId']['videoId']}"
        highlights.append([date, link])

today = datetime.datetime.now().date()

with open("/home/jbg/dev/sports_reminders/2022_kcroyals_schedule.csv", "r") as csv_file:
    data = csv.DictReader(csv_file)

    for x, game in enumerate(data):
        game_day = datetime.datetime.strptime(game["START DATE"], "%m/%d/%y").date()
        if game_day >= today:
            relative_gd = "Today" if game_day == today else "Tomorrow"
            start_time = game["START TIME ET"]
            opponent = game["SUBJECT"].replace("at", "").replace("Royals", "").strip()
            home_away = "Home" if game["LOCATION"] == "Kauffman Stadium - Kansas City" else "Away"
            break

    pd = {
            "token": token,
            "user": user_key,
            "title": f"vs {opponent} ({relative_gd})",
            "message": f"{home_away} @ {start_time}",
            "sound": "intermission",
            "url": highlights[0][1],
            "url_title": f"Highlights from {highlights[0][0]}"
            }
    push_url = 'https://api.pushover.net/1/messages.json'
    pushover = requests.post(push_url, json=pd)



