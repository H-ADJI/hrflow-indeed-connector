# //div[@class='icl-Autocomplete-ariaResultsAvailableWrapper']/span list for locations list
# //input[@id='text-input-where'] input to click for locations
# //ul[@class='icl-Autocomplete-list ']/li//b
# //input DesktopSERPJobAlertPopup-email

import json
from dataclasses import asdict

from playwright.sync_api import Browser, sync_playwright
from playwright_stealth import stealth_sync

from navigation import paginate, visit_job_page
from parsing import extract_details, extract_initial_info

# import sys
# logger.remove()
# logger.add(sys.stderr, level="WARNING")
with sync_playwright() as p:
    browser: Browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",  # noqa
    )
    page = context.new_page()
    details_page = context.new_page()
    stealth_sync(page=page)
    stealth_sync(page=details_page)
    page.goto("https://uk.indeed.com/")
    location_input = page.locator("//input[@id='text-input-where']")
    location_input.fill("Davidstow, Cornwall")
    location_input.press(key="Enter")
    data = []
    try:
        for page_content in paginate(page=page):
            for job_info in extract_initial_info(indeed_feed_page=page_content):
                job_page = visit_job_page(page=details_page, job=job_info)
                data.append(asdict(job_info))
                extract_details(job_page_content=job_page)
    finally:
        with open("jobdata.json", "w") as f:
            json.dump(data, f)
        details_page.screenshot(path="./assets/bugetails.jpg")
        page.screenshot(path="./assets/bugfeed.jpg")
    browser.close()
