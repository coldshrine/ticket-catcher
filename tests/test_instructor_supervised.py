import os
import time
import logging
from typing import Optional
from playwright.sync_api import Page, TimeoutError, sync_playwright
import subprocess
from test_constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlaywrightAutomation:
    def __init__(self, page: Page):
        self.page = page

    def simulate_file_picker(self, file_path: str) -> None:
        folder_path = os.path.dirname(file_path)
        commands = [
            f'xdotool type "{folder_path}"',
            "xdotool key Return"
        ]
        for command in commands:
            time.sleep(1)
            subprocess.run(command, shell=True)
        logger.info(f"Simulated file picker for file: {file_path}")

    def open_login_page(self) -> None:
        try:
            self.page.goto("https://eq.hsc.gov.ua/")
            self.page.wait_for_load_state('domcontentloaded')
            logger.info("Login page loaded successfully.")
        except TimeoutError as e:
            logger.error(f"Timeout while loading login page: {e}")
            raise

    def select_checkbox(self) -> bool:
        try:
            self.page.wait_for_selector('input[type="checkbox"]', timeout=15000)
            checkbox = self.page.locator('input[type="checkbox"]')
            checkbox.click()
            logger.info("Checkbox selected.")
            return True
        except TimeoutError as e:
            logger.error(f"Timeout while selecting checkbox: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while selecting checkbox: {e}")
            return False


    def click_sign_up_button(self) -> None:
        self.page.wait_for_selector('a.btn.btn-lg.btn-hsc-green_s')
        self.page.locator('a.btn.btn-lg.btn-hsc-green_s').click()
        self.page.wait_for_load_state('networkidle')
        logger.info("Sign-up button clicked.")

    def click_electronic_signature_button(self) -> None:
        try:
            self.page.wait_for_selector('a.a1', timeout=15000)
            self.page.locator('a.a1', has_text="Електронного підпису").click()
            self.page.wait_for_load_state('networkidle')
            logger.info("Electronic signature button clicked.")
        except TimeoutError as e:
            logger.error(f"Timeout while clicking electronic signature button: {e}")
            raise

    def upload_file_jks(self, file_path: str) -> None:
        try:
            file_input = self.page.locator('input#PKeyFileInput')
            file_input.set_input_files(file_path)
            logger.info(f"Successfully uploaded file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            raise

    def extract_jks_password(self, file_path: str) -> str:
        try:
            logger.info(f"Extracting password from: {file_path}")
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

    def enter_password(self, password: str) -> None:
        try:
            self.page.wait_for_selector('#PKeyPassword', timeout=15000)
            self.page.wait_for_function(
                'document.querySelector("#PKeyPassword").offsetHeight > 0 && document.querySelector("#PKeyPassword").offsetWidth > 0'
            )
            if not self.page.is_visible('#PKeyPassword') or not self.page.is_enabled('#PKeyPassword'):
                logger.warning("Password field not visible or enabled.")
                return
            time.sleep(1)
            self.page.fill('#PKeyPassword', password)
            logger.info("Password entered.")
            self._click_continue_button()
            time.sleep(5)
            self._click_continue_button()
        except Exception as e:
            logger.error(f"Error during password entry: {e}")
            raise

    def _click_continue_button(self) -> None:
        self.page.wait_for_selector('span.jss177', timeout=15000)
        continue_button = self.page.locator('span.jss177:text("Продовжити")')
        if continue_button.is_visible() and continue_button.is_enabled():
            continue_button.hover()
            time.sleep(0.5)
            continue_button.click()
            logger.info("Clicked 'Продовжити'.")
        else:
            logger.warning("Button not clickable.")

def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        automation = PlaywrightAutomation(page)
        automation.open_login_page()
        automation.select_checkbox()
        automation.click_sign_up_button()
        automation.click_electronic_signature_button()
        automation.upload_file_jks(JKS_FILE_PATH_MAC)
        password = automation.extract_jks_password(PASSWORD_FILE_PATH_MAC)
        logger.info(f"Extracted password: {password}")
        automation.enter_password(password)
        logger.info("Browser session closed.")

if __name__ == "__main__":
    main()
