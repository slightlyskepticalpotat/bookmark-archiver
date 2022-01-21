import argparse
import re
import secrets
import time

import browsercookie
import requests

parser = argparse.ArgumentParser(description="Archives your bookmarks with the Wayback Machine.")
parser.add_argument("bookmark_file", help="A Netscape format bookmarks file", type=str)
arguments = parser.parse_args()
with open(arguments.bookmark_file, "r") as file:
    bookmark_file = file.read()
bookmark_urls = re.findall(r'(?:HREF=\")(.+?)(?:\")', bookmark_file)
cookies = browsercookie.load()

for bookmark_url in bookmark_urls:
    status = requests.get("https://web.archive.org/save/status/user", cookies=cookies, data={"_t": secrets.token_urlsafe(16)}).json()
    while status["available"] == 0:
        print("API Limit: sleeping for 120 seconds")
        time.sleep(120)
        status = requests.get("https://web.archive.org/save/status/user", cookies=cookies, data={"_t": secrets.token_urlsafe(16)}).json()
    print(f"Capturing: {bookmark_url}")
    capture = requests.post(f"https://web.archive.org/save", cookies=cookies, data={"url": bookmark_url, "capture_all": "1", "capture_outlinks": "0", "capture_screenshot": "0", "delay_wb_availability": "0", "skip_first_archive": "1", "if_not_archived_within": "0", "email_result": "0"})
