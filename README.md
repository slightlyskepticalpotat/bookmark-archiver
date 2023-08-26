# bookmark-archiver
Python script that archives all of your bookmarks on the Internet Archive. Supports all major browsers. Contributions welcome!

bookmarkarchiver uses the official Save Page Now [API](https://docs.google.com/document/d/1Nsv52MvSjbLb2PCpHlat0gkzw0EvtSgpKHu4mk0MnrA). Anonymous users are limited to 4,000 requests per day, which should be enough to save around 200 websites. If you create a free account to the [Internet Archive](https://archive.org/) and log in with a Chromium-based browser (e.g. Google Chrome) or Firefox, your single-day request limit increases to 100,000 and you should be able to save approximately 5000 websites. This may be significant overestimate if you also choose to captire outlinks. Due to API limitations, each bookmark should take around 10 seconds to archive.

bookmarkarchiver uses the [browser_cookie3](https://github.com/borisbabic/browser_cookie3) module.

## Usage
To use bookmarkarchiver, you need a bookmark file. You can get one by exporting them from a browser—instructions vary by browser and are readily available online. Typically, you have to export them through your browser's bookmarks page.

The easiest way to install bookmarkarchiver is to run `pip3 install bookmark-archiver`.

```
$ pip3 install -r requirements.txt
$ python3 bookmarkarchiver.py --help
usage: bookmarkarchiver.py [-h] [--no_capture_all] [--capture_outlinks] [--capture_screenshot] [--delay_wb_availability] [--force_get]
                           [--no_skip_first_archive] [--email_result] [--quit_immediately] [--api_wait_seconds API_WAIT_SECONDS]
                           bookmark_file

Archives your bookmarks with the Wayback Machine.

positional arguments:
  bookmark_file         A Netscape format bookmarks file

optional arguments:
  -h, --help            show this help message and exit
  --no_capture_all, -n  Don't capture error pages
  --capture_outlinks, -c
                        Capture all outlinks
  --capture_screenshot, -s
                        Capture a screenshot
  --delay_wb_availability, -d
                        Delay uploading capture
  --force_get, -f       Force a GET request
  --no_skip_first_archive, -a
                        Don't recapture pages
  --email_result, -e    Email results to user
  --quit_immediately, -q
                        Don't show end results
  --api_wait_seconds API_WAIT_SECONDS, -w API_WAIT_SECONDS
```
