"""Python script that archives all of your bookmarks on the Internet Archive. Supports all major browsers."""

import argparse
import re
import secrets
import time

import requests
import json

import browser_cookie3


JSON_HEADER = {"Accept":  "application/json"}
KNOWN_ERRORS = (KeyError, requests.exceptions.ConnectionError, json.JSONDecodeError)
START_TIME = time.time()


def wait_for_api(available):
    """Wait until there are a number of free concurrent requests."""
    wait_time = 1
    status = requests.get("https://web.archive.org/save/status/user", data={"_t": secrets.token_urlsafe(16)}, cookies=cookies, headers=JSON_HEADER).json()
    while status["available"] < available:
        print(f"API Limit: sleeping for {wait_time} seconds")
        time.sleep(wait_time)
        wait_time *= 2
        status = requests.get("https://web.archive.org/save/status/user", data={"_t": secrets.token_urlsafe(16)}, cookies=cookies, headers=JSON_HEADER).json()

def main():
    # parse and validate command-line arguments
    parser = argparse.ArgumentParser(description="Archives your bookmarks with the Wayback Machine.")
    parser.add_argument("bookmark_file", help="A Netscape format bookmarks file", type=str)
    parser.add_argument("--no_capture_all", "-n", default=True, action="store_false", help="Don't capture error pages")
    parser.add_argument("--capture_outlinks", "-c", default=False, action="store_true", help="Capture all outlinks")
    parser.add_argument("--capture_screenshot", "-s", default=False, action="store_true", help="Capture a screenshot")
    parser.add_argument("--delay_wb_availability", "-d", default=False, action="store_true", help="Delay uploading capture")
    parser.add_argument("--force_get", "-f", default=False, action="store_true", help="Force a GET request")
    parser.add_argument("--no_skip_first_archive", "-a", default=True, action="store_false", help="Don't recapture pages")
    parser.add_argument("--email_result", "-e", default=False, action="store_true", help="Email results to user")
    parser.add_argument("--quit_immediately", "-q", default=False, action="store_true", help="Don't show end results")
    parser.add_argument("--api_wait_seconds", "-w", default=8, type=int)
    arguments = vars(parser.parse_args())
    assert arguments["api_wait_seconds"] >= 0, "api_wait_seconds cannot be negative"

    data = {"bookmark_file": arguments["bookmark_file"]}
    for key in arguments.keys():
        if arguments[key] is True and key not in ["api_wait_seconds"]:
            data[key] = str(int(arguments[key]))
    print("Setting Up: command-line arguments processed")

    # parse netscape-format bookmark file
    with open(data['bookmark_file'], "r", encoding="utf-8") as file:
        bookmark_file = file.read()
    bookmark_urls = re.findall(r'(?:HREF=\")(.+?)(?:\")', bookmark_file)
    bookmark_names = re.findall(r'(?:\">)(.+?)(?:</A>)', bookmark_file)
    bookmarks = [{"name": bookmark_names[i], "url": bookmark_urls[i]} for i in range(len(bookmark_urls))]
    print(f"Setting Up: {len(bookmarks)} browser bookmarks queued")

    # load cookies from chrome or firefox
    global cookies
    cookies = browser_cookie3.load()
    print("Setting Up: chrome/firefox cookies loaded")

    # try to save every bookmark
    for bookmark in bookmarks:
        try:
            wait_for_api(1)
            print(f"Capturing: {bookmark['name']}")
            data["url"] = bookmark["url"]
            request = requests.post("https://web.archive.org/save", data=data, cookies=cookies, headers=JSON_HEADER).json()
            bookmark["job_id"] = request["job_id"]
        except KNOWN_ERRORS as error:
            print(f"Error: {request.get('status_ext', 'unknown network error')}")
            print(f"Error: {str(error)} during processing")
            try: # shortened version, retries
                wait_for_api(1)
                print(f"Retrying: {bookmark['name']}")
                request = requests.post("https://web.archive.org/save", data=data, cookies=cookies, headers=JSON_HEADER).json()
                bookmark["job_id"] = request["job_id"]
            except KNOWN_ERRORS as error:
                print(f"Error: {request.get('status_ext', 'unknown network error')}")
                print(f"Error: {str(error)} during retry")
        time.sleep(arguments["api_wait_seconds"]) # needed because the api lags

    # short-circuit and quit
    if arguments["quit_immediately"]:
        raise SystemExit

    # clean up and actually quit
    print("Finishing: waiting for completion")
    wait_for_api(6)
    job_ids = [bookmark.get("job_id", "placeholder-job-id") for bookmark in bookmarks]
    job_ids = [requests.get(f"https://web.archive.org/save/status/{job_id}", cookies=cookies, headers=JSON_HEADER).json()["status"] for job_id in job_ids]
    print(f"Information: {len(job_ids)} bookmarks in total")
    print(f"Information: {job_ids.count('success')} bookmarks archived")
    if len(job_ids) - job_ids.count("success"):
        print(f"Information: {len(job_ids) - job_ids.count('success')} failed; check logs")
        for i, job_id in enumerate(job_ids):
            if job_id != "success":
                print(f"Information: {bookmarks[i]['name']} failed, status {job_id}")
    print(f"Information: finished in {time.time() - START_TIME} seconds")

if __name__ == "__main__":
    main()
