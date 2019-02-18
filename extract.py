import os
import re
import json

import requests


URL_REGEX = r'https?://youtu[^"<\n]+'

with open("good-vibes.html") as f:
    content = f.read()

sorted_dict = {u[-11:]: {"id": u[-11:]} for u in re.findall(URL_REGEX, content)}

for e in json.load(open("data.json", "r")):
    sorted_dict[e["id"]] = e

KEY = os.getenv("YOUTUBE_KEY")
for i, obj in sorted_dict.items():
    if "title" in obj:
        continue
    url = f"https://www.googleapis.com/youtube/v3/videos?id={i}&part=snippet&key={KEY}"
    r = requests.get(url).json()
    title = r["items"][0]["snippet"]["title"]
    obj["title"] = title

print(json.dumps(list(sorted_dict.values()), indent=2))
