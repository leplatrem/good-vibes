import re
import json

URL_REGEX = r'https?://youtu[^"<\n]+'

with open("good-vibes.html") as f:
    content = f.read()

sorted_dict = {u: u for u in re.findall(URL_REGEX, content)}
urls = [u.rsplit("/")[-1] for u in sorted_dict.keys()]

print("\n".join(["{ id: \"%s\" }," % u for u in urls]))
