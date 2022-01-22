# bookmarkarchiver
Python script that archives all of your bookmarks on the Internet Archive. Supports all major browsers.

bookmarkarchiver uses the official Save Page Now [API](https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA). Anonymous users are limited to 4,000 requests per day, which should be enough to save around 200 websites. If you create a free account to the [Internet Archive](https://archive.org/) and log in with Chrome, Chromium, or Firefox, your single-day request limit increases to 100,000 and you should be able to save approximately 5000 websites.

As for dependencies, bookmarkarchiver uses Richard Penman's [browsercookie](https://github.com/richardpenman/browsercookie) module with [this patch](https://github.com/richardpenman/browsercookie/pull/8/commits/badb6e122d8ff24b3494babf74e1a4dad1538f8e) applied. It also uses the Python [requests](https://docs.python-requests.org/en/latest/) library.

## Usage
To use bookmarkarchiver, you need a bookmark file. You can get one by exporting them from a browser—instructions are online.
```
$ pip3 -r requirements.txt
$ python3 bookmarkarchiver.py --help
usage: bookmarkarchiver.py [-h] [--capture_all] [--capture_outlinks] [--capture_screenshot] [--delay_wb_availability] [--force_get]
                           [--skip_first_archive] [--email_result] [--quit_immediately]
                           bookmark_file

Archives your bookmarks with the Wayback Machine.

positional arguments:
  bookmark_file         A Netscape format bookmarks file

optional arguments:
  -h, --help            show this help message and exit
  --capture_all, -a     Don't capture error pages
  --capture_outlinks, -o
                        Capture all outlinks
  --capture_screenshot, -s
                        Capture a screenshot
  --delay_wb_availability, -d
                        Delay uploading capture
  --force_get, -g       Force a GET request
  --skip_first_archive, -f
                        Don't find old captures
  --email_result, -e    Email results to user
  --quit_immediately, -q
                        Don't show end results
```

## To-Do
- publish as a pip package
