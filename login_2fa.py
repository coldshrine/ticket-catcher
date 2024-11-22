import time
from playwright.sync_api import sync_playwright, TimeoutError

from constants import JKS_FILE_PATH

def open_login_page(page):
    """
    Opens the login page.
    """
    try:
        page.goto("https://eq.hsc.gov.ua/")
        page.wait_for_load_state('domcontentloaded')  # Ensuring the page is loaded properly
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
    Uploads a .jks file to the file input (dropbox) on the page.

    Args:
    - page: The Playwright page object
    - file_path: The full path to the .jks file to be uploaded
    """
    try:
        # Wait for the span element to be visible and clickable, which triggers the file input dialog
        page.wait_for_selector('span.jss525:visible', timeout=20000)  # Adjust the selector if necessary
        
        # Click the span element by its exact text content
        page.locator('span:has-text("оберіть його на своєму носієві")').click()
        
        # Wait for the file input element to be visible
        page.wait_for_timeout(2000)  # Wait for 2 seconds to ensure the file input appears
        
        # Attempt to find and interact with the file input element
        page.wait_for_selector('input[type="file"]:visible', timeout=20000)
        
        # Assuming there are multiple file input elements, adjust the index as per your observation
        file_input = page.locator('input[type="file"]:visible').nth(0)  # Use nth(0) if it's the first visible file input
        file_input.set_input_files(file_path)
        
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

        # Navigate to the page (assuming you are already there)
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
