import argparse
import re
import secrets
import time

import requests

import browsercookie

def wait_for_api(n):
    """Wait until there are n available concurrent requests."""
    wait_time = 1
    status = requests.get("https://web.archive.org/save/status/user", data={"_t": secrets.token_urlsafe(16)}, cookies=cookies, headers={"Accept": "application/json"}).json()
    while status["available"] < n:
        print(f"API Limit: sleeping for {wait_time} seconds")
        time.sleep(wait_time)
        wait_time *= 2
        status = requests.get("https://web.archive.org/save/status/user", data={"_t": secrets.token_urlsafe(16)}, cookies=cookies, headers={"Accept": "application/json"}).json()

# parse and validate command-line arguments
parser = argparse.ArgumentParser(description="Archives your bookmarks with the Wayback Machine.")
parser.add_argument("bookmark_file", help="A Netscape format bookmarks file", type=str)
parser.add_argument("--capture_all", "-a", default=True, action="store_false", help="Don't capture error pages")
parser.add_argument("--capture_outlinks", "-o", default=False, action="store_true", help="Capture all outlinks")
parser.add_argument("--capture_screenshot", "-s", default=False, action="store_true", help="Capture a screenshot")
parser.add_argument("--delay_wb_availability", "-d", default=False, action="store_true", help="Delay uploading capture")
parser.add_argument("--force_get", "-g", default=False, action="store_true", help="Force a GET request")
parser.add_argument("--skip_first_archive", "-f", default=True, action="store_false", help="Don't recapture pages")
parser.add_argument("--email_result", "-e", default=False, action="store_true", help="Email results to user")
parser.add_argument("--quit_immediately", "-q", default=False, action="store_true", help="Don't show end results")
arguments = vars(parser.parse_args())
data = {"bookmark_file": arguments["bookmark_file"]}
for key in arguments.keys():
    if arguments[key] is True:
        data[key] = str(int(arguments[key]))
print("Setting Up: command-line arguments loaded")

# parse netscape-format bookmark file
with open(data['bookmark_file'], "r", encoding="utf-8") as file:
    bookmark_file = file.read()
bookmark_urls = re.findall(r'(?:HREF=\")(.+?)(?:\")', bookmark_file)
bookmark_names = re.findall(r'(?:\">)(.+?)(?:</A>)', bookmark_file)
bookmarks = [{"name": bookmark_names[i], "url": bookmark_urls[i]} for i in range(len(bookmark_urls))]
print(f"Setting Up: {len(bookmarks)} browser bookmarks loaded")

# load cookies from chrome or firefox
cookies = browsercookie.load()
print("Setting Up: chrome/firefox cookies loaded")

# try to save every bookmark
for bookmark in bookmarks:
    try:
        wait_for_api(1)
        print(f"Capturing: {bookmark['name']}")
        data["url"] = bookmark["url"]
        request = requests.post("https://web.archive.org/save", data=data, cookies=cookies, headers={"Accept": "application/json"}).json()
        bookmark["job_id"] = request["job_id"]
    except KeyError as error:
        print(f"Error: {request['status_ext']}")
        print(f"Error: {str(error)} during processing")
        print("Recovery: sleeping for 10 seconds")
        time.sleep(10)

# short-circuit and quit
if arguments["quit_immediately"]:
    raise SystemExit

# clean up and actually quit
print("Finishing: waiting for completion")
wait_for_api(6)
job_ids = [bookmark.get("job_id", "placeholder-job-id") for bookmark in bookmarks]
job_ids = [requests.get(f"https://web.archive.org/save/status/{job_id}", cookies=cookies, headers={"Accept": "application/json"}).json()["status"] for job_id in job_ids]
print(f"Information: {len(job_ids)} bookmarks in total")
print(f"Information: {job_ids.count('success')} bookmarks archived")
