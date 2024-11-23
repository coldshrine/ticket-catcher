import os
import time
import logging
from playwright.sync_api import sync_playwright, TimeoutError
import subprocess

from constants import JKS_FILE_PATH, PASSWORD_FILE_PATH


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulate_file_picker(file_path):
    folder_path = os.path.dirname(file_path)
    commands = [
        f'xdotool type "{folder_path}"',
        "xdotool key Return"
    ]
    for command in commands:
        time.sleep(1)
        subprocess.run(command, shell=True)
    logger.info(f"Simulated file picker for file: {file_path}")

def open_login_page(page):
    try:
        page.goto("https://eq.hsc.gov.ua/")
        page.wait_for_load_state('domcontentloaded')
        logger.info("Login page loaded successfully.")
    except TimeoutError as e:
        logger.error(f"Timeout while loading login page: {e}")
        raise

def select_checkbox(page):
    try:
        page.wait_for_selector('input[type="checkbox"]', timeout=5000)
        page.locator('input[type="checkbox"]').click()
        logger.info("Checkbox selected.")
    except TimeoutError as e:
        logger.error(f"Timeout while selecting checkbox: {e}")
        raise

def click_sign_up_button(page):
    page.wait_for_selector('a.btn.btn-lg.btn-hsc-green_s')
    page.locator('a.btn.btn-lg.btn-hsc-green_s').click()
    page.wait_for_load_state('networkidle')
    logger.info("Sign-up button clicked.")

def click_electronic_signature_button(page):
    try:
        page.wait_for_selector('a.a1', timeout=5000)
        page.locator('a.a1', has_text="Електронного підпису").click()
        page.wait_for_load_state('networkidle')
        logger.info("Electronic signature button clicked.")
    except TimeoutError as e:
        logger.error(f"Timeout while clicking electronic signature button: {e}")
        raise

def upload_file_jks(page, file_path):
    try:
        page.wait_for_selector('span:has-text("оберіть його на своєму носієві")', timeout=20000)
        page.locator('span:has-text("оберіть його на своєму носієві")').click()
        simulate_file_picker(file_path)
        logger.info(f"Successfully uploaded file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to upload file {file_path}: {e}")
        raise

def extract_jks_password(file_path):
    try:
        with open(file_path, 'r') as file:
            password = file.read().strip()
        logger.info("Password extracted successfully.")
        return password
    except FileNotFoundError:
        logger.error(f"Password file not found at {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error reading password file: {e}")
        raise

def enter_password(page, password):
    try:
        page.wait_for_selector('#PKeyPassword', timeout=5000)
        page.wait_for_function('document.querySelector("#PKeyPassword").offsetHeight > 0 && document.querySelector("#PKeyPassword").offsetWidth > 0')
        if not page.is_visible('#PKeyPassword') or not page.is_enabled('#PKeyPassword'):
            logger.warning("Password field not visible or enabled.")
            return
        time.sleep(1)
        page.fill('#PKeyPassword', password)
        logger.info("Password entered.")

        def click_continue_button():
            page.wait_for_selector('span.jss177', timeout=5000)
            continue_button = page.locator('span.jss177:text("Продовжити")')
            if continue_button.is_visible() and continue_button.is_enabled():
                continue_button.hover()
                time.sleep(0.5)
                continue_button.click()
                logger.info("Clicked 'Продовжити'.")
            else:
                logger.warning("Button not clickable.")

        click_continue_button()
        time.sleep(5)
        click_continue_button()
    except Exception as e:
        logger.error(f"Error during password entry: {e}")
        raise

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        open_login_page(page)
        select_checkbox(page)
        click_sign_up_button(page)
        click_electronic_signature_button(page)
        upload_file_jks(page, JKS_FILE_PATH)
        password = extract_jks_password(PASSWORD_FILE_PATH)
        logger.info(f"Extracted password: {password}")
        enter_password(page, password)
        time.sleep(20)
        browser.close()
        logger.info("Browser session closed.")

if __name__ == "__main__":
    main()
