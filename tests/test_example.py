import re
import time
from playwright.sync_api import sync_playwright, expect
import pytest

def test_has_title(page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
    time.sleep(2)  # Wait for 2 seconds to see the result

def test_get_started_link(page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
    time.sleep(5)  # Wait for 2 seconds to see the result

# If you want to call them manually
if __name__ == "__main__":
    # Launch the browser in headed mode (with UI visible)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=False to see the browser
        page = browser.new_page()
        test_has_title(page)
        test_get_started_link(page)
        browser.close()
