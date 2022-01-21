import argparse
import re
import secrets
import time

import requests
import browsercookie

wait_time = 1

# parse and validate command-line arguments
parser = argparse.ArgumentParser(description="Archives your bookmarks with the Wayback Machine.")
parser.add_argument("bookmark_file", help="A Netscape format bookmarks file", type=str)
parser.add_argument("--capture_all", "-a", default=True, action="store_false", help="Don't capture error pages")
parser.add_argument("--capture_outlinks", "-o", default=False, action="store_true", help="Capture all outlinks")
parser.add_argument("--capture_screenshot", "-s", default=False, action="store_true", help="Capture a screenshot")
parser.add_argument("--delay_wb_availability", "-d", default=False, action="store_true", help="Delay uploading capture")
parser.add_argument("--force_get", "-g", default=False, action="store_true", help="Force a GET request")
parser.add_argument("--skip_first_archive", "-f", default=True, action="store_false", help="Don't find old captures")
parser.add_argument("--email_result", "-e", default=False, action="store_true", help="Email results to user")
arguments = vars(parser.parse_args())
data = {"bookmark_file": arguments["bookmark_file"]}
for key in arguments.keys():
    if arguments[key] is True:
        data[key] = str(int(arguments[key]))
print("Setup: command-line arguments loaded")

# parse netscape-format bookmark file
with open(data['bookmark_file'], "r", encoding="utf-8") as file:
    bookmark_file = file.read()
bookmark_urls = re.findall(r'(?:HREF=\")(.+?)(?:\")', bookmark_file)
bookmark_names = re.findall(r'(?:\">)(.+?)(?:</A>)', bookmark_file)
bookmarks = [{"name": bookmark_names[i], "url": bookmark_urls[i]} for i in range(len(bookmark_urls))]
print(f"Setup: {len(bookmarks)} bookmarks loaded")

# load cookies from chrome or firefox
cookies = browsercookie.load()
print("Setup: chrome/firefox cookies loaded")

for bookmark in bookmarks:
    status = requests.get("https://web.archive.org/save/status/user", data={"_t": secrets.token_urlsafe(16)}, cookies=cookies).json()
    while status["available"] == 0:
        print(f"API Limit: sleeping for {wait_time} seconds")
        time.sleep(wait_time)
        wait_time *= 2
        status = requests.get("https://web.archive.org/save/status/user", data={"_t": secrets.token_urlsafe(16)}, cookies=cookies).json()
    wait_time = 1
    print(f"Capturing: {bookmark['name']}")
    data["url"] = bookmark["url"]
    requests.post("https://web.archive.org/save", data=data, cookies=cookies)
