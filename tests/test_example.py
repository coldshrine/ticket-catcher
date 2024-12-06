import re
import time
from playwright.sync_api import sync_playwright, expect
import pytest

def test_has_title(page):
    page.goto("https://playwright.dev/")
    expect(page).to_have_title(re.compile("Playwright"))
    time.sleep(2)

def test_get_started_link(page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
    time.sleep(5)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        test_has_title(page)
        test_get_started_link(page)
        browser.close()
