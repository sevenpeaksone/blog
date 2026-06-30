import sys, glob
from playwright.sync_api import sync_playwright

BASE = "/sessions/ecstatic-youthful-edison/mnt/ai-blog/output/news-정치사회/images"
SRC = BASE + "/_src"

jobs = [
    ("thumbnail.html", "thumbnail.png"),
    ("body-1.html", "body-1.png"),
    ("body-2.html", "body-2.png"),
    ("body-3.html", "body-3.png"),
    ("body-4.html", "body-4.png"),
    ("body-5.html", "body-5.png"),
]
if len(sys.argv) > 1:
    only = set(sys.argv[1:])
    jobs = [j for j in jobs if j[1].replace(".png","") in only or j[1] in only]

def launch(p):
    # try headless-shell channel
    try:
        return p.chromium.launch(channel="chromium-headless-shell", args=["--no-sandbox"])
    except Exception as e:
        print("headless-shell channel failed:", str(e)[:120])
    # try glob executable
    paths = glob.glob("/sessions/ecstatic-youthful-edison/.cache/ms-playwright/chromium_headless_shell-*/**/headless_shell", recursive=True)
    if paths:
        try:
            return p.chromium.launch(executable_path=paths[0], args=["--no-sandbox"])
        except Exception as e:
            print("headless_shell exec failed:", str(e)[:120])
    # full chromium channel
    return p.chromium.launch(channel="chromium", args=["--no-sandbox"])

with sync_playwright() as p:
    browser = launch(p)
    for html, out in jobs:
        page = browser.new_page(device_scale_factor=2)
        page.goto("file://" + SRC + "/" + html)
        page.wait_for_timeout(400)
        page.locator("#card").screenshot(path=BASE + "/" + out)
        page.close()
        print("captured", out)
    browser.close()
print("ALL DONE")
