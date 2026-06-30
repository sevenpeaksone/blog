import glob, sys
from playwright.sync_api import sync_playwright

DIR = "/sessions/ecstatic-youthful-edison/mnt/ai-blog/output/news-경제/images"

def launch(p):
    try:
        return p.chromium.launch(channel='chromium-headless-shell', args=['--no-sandbox'])
    except Exception:
        paths = glob.glob('/sessions/ecstatic-youthful-edison/.cache/ms-playwright/chromium_headless_shell-*/**/headless_shell', recursive=True)
        return p.chromium.launch(executable_path=paths[0], args=['--no-sandbox'])

jobs = [
    ("_src_thumbnail.html", "thumbnail.png", 1080),
    ("_src_body-1.html", "body-1.png", 960),
    ("_src_body-2.html", "body-2.png", 900),
    ("_src_body-3.html", "body-3.png", 960),
    ("_src_body-4.html", "body-4.png", 960),
    ("_src_body-5.html", "body-5.png", 960),
]

only = set(sys.argv[1:]) if len(sys.argv) > 1 else None

with sync_playwright() as p:
    b = launch(p)
    for html, png, w in jobs:
        if only and png not in only:
            continue
        page = b.new_page(viewport={"width": w, "height": 1200}, device_scale_factor=2)
        page.goto(f"file://{DIR}/{html}")
        page.wait_for_timeout(400)
        page.locator("#card").screenshot(path=f"{DIR}/{png}")
        print("captured", png)
        page.close()
    b.close()
print("ALL DONE")
