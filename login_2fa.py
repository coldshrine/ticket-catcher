import os
import time
from playwright.sync_api import sync_playwright, TimeoutError
from constants import JKS_FILE_PATH
import subprocess

def simulate_file_picker(file_path):
    """
    Simulates navigation and selection in the file picker using xdotool.

    Args:
    - file_path: The full path to the file to be selected.
    """
    folder_path = os.path.dirname(file_path)

    # Simulate navigation in the file picker
    commands = [
        f'xdotool type "{folder_path}"',  # Type the folder path
        "xdotool key Return"             # Press Enter to select the file
    ]

    for command in commands:
        time.sleep(1)
        subprocess.run(command, shell=True)

def open_login_page(page):
    """
    Opens the login page.
    """
    try:
        page.goto("https://eq.hsc.gov.ua/")
        page.wait_for_load_state('domcontentloaded')
    except TimeoutError as e:
        print(f"Timeout while loading login page: {e}")
        raise

def select_checkbox(page):
    """
    Selects the checkbox near the text "Я ознайомлений та погоджуюсь з умовами надання послуги".
    """
    try:
        page.wait_for_selector('input[type="checkbox"]', timeout=5000)
        checkbox = page.locator('input[type="checkbox"]')
        checkbox.click()
    except TimeoutError as e:
        print(f"Timeout while selecting checkbox: {e}")
        raise

def click_sign_up_button(page):
    """
    Clicks the "е-запис" button after the checkbox is selected.
    """
    page.wait_for_selector('a.btn.btn-lg.btn-hsc-green_s')
    button = page.locator('a.btn.btn-lg.btn-hsc-green_s')
    button.click()
    
    # Wait for the page to load or stabilize after the click
    page.wait_for_load_state('networkidle')  # This waits for network activity to settle

def click_electronic_signature_button(page):
    """
    Clicks the "Електронного підпису" button after navigating to the next page.
    """
    try:
        # Wait for the link with the exact text "Електронного підпису"
        page.wait_for_selector('a.a1', timeout=5000)  # Wait for any matching <a> elements
        sign_button = page.locator('a.a1', has_text="Електронного підпису")  # Match link by text content
        sign_button.click()
        
        # Wait for the page to stabilize after clicking the link
        page.wait_for_load_state('networkidle')  # Wait for the page to be idle (no ongoing network activity)
    except TimeoutError as e:
        print(f"Timeout while clicking electronic signature button: {e}")
        raise

def upload_jks_file(page, file_path):
    """
    Uploads a .jks file to the file input element on the page.

    Args:
    - page: The Playwright page object.
    - file_path: The full path to the .jks file to be uploaded.
    """
    try:
        # Wait for the span element to appear and click it
        page.wait_for_selector('span:has-text("оберіть його на своєму носієві")', timeout=20000)
        page.locator('span:has-text("оберіть його на своєму носієві")').click()

        # Use xdotool to simulate file selection in the file picker
        simulate_file_picker(file_path)
        
        print(f"Successfully uploaded the file: {file_path}")
    except Exception as e:
        print(f"Failed to upload the file due to: {e}")
        raise

def main():
    """
    Main function to automate the process, focusing on file upload.
    """
    with sync_playwright() as p:
        # Launch the browser (set headless=False to see UI)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to the page
        open_login_page(page)
        select_checkbox(page)
        click_sign_up_button(page)
        click_electronic_signature_button(page)

        # Upload the .jks file after navigating
        upload_jks_file(page, JKS_FILE_PATH)

        # Sleep for a few seconds to allow any actions to complete before closing
        time.sleep(20)

        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()
