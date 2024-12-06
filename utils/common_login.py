import os
import time
import logging
from playwright.sync_api import TimeoutError
import subprocess

from utils.constants import SELECTORS

logging.basicConfig(level=logging.INFO)
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

def wait_and_click(page, selector, timeout=15000, description=""):
    try:
        page.wait_for_selector(selector, timeout=timeout)
        element = page.locator(selector)
        if element.is_visible() and element.is_enabled():
            element.click()
            logger.info(f"{description} clicked successfully.")
        else:
            logger.warning(f"{description} is not clickable.")
    except TimeoutError:
        logger.error(f"Timeout while waiting for {description} to appear.")
        raise
    except Exception as e:
        logger.error(f"Error while interacting with {description}: {e}")
        raise

def open_login_page(page):
    try:
        page.goto("https://eq.hsc.gov.ua/")
        page.wait_for_load_state('domcontentloaded')
        logger.info("Login page loaded successfully.")
    except TimeoutError as e:
        logger.error(f"Timeout while loading login page: {e}")
        raise

def select_checkbox(page):
    wait_and_click(page, SELECTORS["checkbox"], description="Checkbox")

def click_sign_up_button(page):
    wait_and_click(page, SELECTORS["sign_up_button"], description="Sign-up button")

def click_electronic_signature_button(page):
    wait_and_click(page, SELECTORS["electronic_signature"], description="Electronic signature button")

def upload_file_jks(page, file_path):
    try:
        file_input = page.locator('input#PKeyFileInput')
        file_input.set_input_files(file_path)
        logger.info(f"Successfully uploaded file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to upload file {file_path}: {e}")
        raise

def extract_jks_password(file_path):
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

def enter_password(page, password):
    try:
        wait_and_click(page, SELECTORS["password_field"], description="Password field")
        page.fill(SELECTORS["password_field"], password)
        logger.info("Password entered.")
        wait_and_click(page, SELECTORS["continue_button"], description="Continue button")
    except Exception as e:
        logger.error(f"Error during password entry: {e}")
        raise

def zpysatys_button(page):
    wait_and_click(page, SELECTORS["signup_button"], description="Sign-up button")

def select_practical_exam_link(page):
    wait_and_click(page, SELECTORS["practical_exam_link"], description="Practical exam link")

def click_first_date_link(page):
    wait_and_click(page, SELECTORS["first_date_button"], description="First date button")

def click_and_check_talons(page):
    try:
        right_clicks, left_clicks = 0, 0

        while True:
            if right_clicks < 18:
                wait_and_click(page, SELECTORS["right_arrow"], description="Right arrow")
                right_clicks += 1
            else:
                wait_and_click(page, SELECTORS["left_arrow"], description="Left arrow")
                left_clicks += 1
                if left_clicks == 18:
                    right_clicks, left_clicks = 0, 0

            if page.locator(SELECTORS["talon_present"]).is_visible():
                logger.info("Available talons found.")
                break

            logger.info("No talon found. Retrying in 2 seconds...")
            time.sleep(2)
    except Exception as e:
        logger.error(f"Error while clicking talons: {e}")
        raise
