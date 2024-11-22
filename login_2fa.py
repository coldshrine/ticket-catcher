import time
from playwright.sync_api import sync_playwright

def open_login_page(page):
    """
    Opens the login page.
    """
    page.goto("https://eq.hsc.gov.ua/")

def select_checkbox(page):
    """
    Selects the checkbox near the text "Я ознайомлений та погоджуюсь з умовами надання послуги".
    """
    page.wait_for_selector('input[type="checkbox"]')
    checkbox = page.locator('input[type="checkbox"]')
    checkbox.click()

def click_sign_up_button(page):
    """
    Clicks the "е-запис" button after the checkbox is selected.
    """
    page.wait_for_selector('a.btn.btn-lg.btn-hsc-green_s')
    button = page.locator('a.btn.btn-lg.btn-hsc-green_s')
    button.click()

def main():
    """
    Main function to automate the process.
    """
    with sync_playwright() as p:
        # Launch the browser (set headless=False to see UI)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        open_login_page(page)
        # Select the checkbox

        select_checkbox(page)
        time.sleep(10)

        # Click the "е-запис" button
        click_sign_up_button(page)
        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    main()
