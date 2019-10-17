"""

1. Open WhatsApp Web
2. Use Browser DevTools
3. Save HTML to file on disk
4. Run
```
$ YOUTUBE_KEY=AIzaSy...0Yc python3 extract.py < good-vibes.html
```
5. `git commit -a`
6. `git push origin gh-pages`

* See https://console.developers.google.com/apis/api/youtube.googleapis.com/

"""
import json
import os
import re
import sys

import requests


JSON_FILE = "data.json"
KEY = os.getenv("YOUTUBE_KEY")
YOUTUBE_URL = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&key={KEY}&id="
URL_REGEX = r'https?://youtu[^\?&"<\n]{11,}'

# Load previous videos
by_id = {}
with open(JSON_FILE, "r") as f:
    for e in json.load(f):
        by_id[e["id"]] = e

# Read HTML from stdin
content = sys.stdin.read()

# Parse HTML like it's 1992.
urls = set(re.findall(URL_REGEX, content))

for url in urls:
    vid = url[-11:]

    if vid in by_id:
        print(vid, "Skip duplicate")
        continue

    try:
        r = requests.get(YOUTUBE_URL + vid).json()
        title = r["items"][0]["snippet"]["title"]

        by_id[vid] = {
            "id": vid,
            "title": title,
        }
        print(vid, title)

    except:
        print(vid, r, file=sys.stderr)
        raise

# Overwrite with new list
with open(JSON_FILE, "w") as f:
    json.dump(list(by_id.values()), f, indent=2)
