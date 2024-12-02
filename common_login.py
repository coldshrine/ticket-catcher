import os
import time
import logging
from playwright.sync_api import sync_playwright, TimeoutError
import subprocess

from constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC

# Configure logging
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
        logger.info("Waiting for checkbox to be visible...")
        page.wait_for_selector('input[type="checkbox"]', timeout=100000)  # Increase timeout
        checkbox = page.locator('input[type="checkbox"]')
        
        # Check if the checkbox is visible and enabled before clicking
        if checkbox.is_visible() and checkbox.is_enabled():
            checkbox.click()
            logger.info("Checkbox selected.")
        else:
            logger.warning("Checkbox is either not visible or not enabled.")
    except TimeoutError as e:
        logger.error(f"Timeout while selecting checkbox: {e}")
        raise

def click_sign_up_button(page):
    try:
        page.wait_for_selector('a.btn.btn-lg.btn-hsc-green_s')
        page.locator('a.btn.btn-lg.btn-hsc-green_s').click()
        page.wait_for_load_state('networkidle')
        logger.info("Sign-up button clicked.")
    except TimeoutError as e:
        logger.error(f"Timeout while clicking sign-up button: {e}")
        raise

def click_electronic_signature_button(page):
    try:
        page.wait_for_selector('a.a1', timeout=15000)
        page.locator('a.a1', has_text="Електронного підпису").click()
        page.wait_for_load_state('networkidle')
        logger.info("Electronic signature button clicked.")
    except TimeoutError as e:
        logger.error(f"Timeout while clicking electronic signature button: {e}")
        raise

def upload_file_jks(page, file_path):
    try:
        file_input = page.locator('input#PKeyFileInput')  # Locator for JKS file input
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
        page.wait_for_selector('#PKeyPassword', timeout=15000)
        page.wait_for_function('document.querySelector("#PKeyPassword").offsetHeight > 0 && document.querySelector("#PKeyPassword").offsetWidth > 0')
        if not page.is_visible('#PKeyPassword') or not page.is_enabled('#PKeyPassword'):
            logger.warning("Password field not visible or enabled.")
            return
        time.sleep(1)
        page.fill('#PKeyPassword', password)
        logger.info("Password entered.")

        def click_continue_button():
            page.wait_for_selector('span.jss177', timeout=15000)
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

def zpysatys_button(page):
    try:
        button_selector = page.get_by_role("button", name="Записатись")
        buttons_count = button_selector.count()
        if buttons_count != 1:
            logger.error(f"Expected 1 button but found {buttons_count} for selector 'Записатись'.")
            return
        
        button_selector.click()
        logger.info("Sign-up button clicked successfully.")
    except Exception as e:
        logger.error(f"Failed to click the sign-up button: {e}")

def select_practical_exam_link(page):
    try:
        link_selector = page.get_by_role("link", name="Практичний іспит")
        
        links_count = link_selector.count()
        if links_count != 1:
            logger.error(f"Expected 1 link but found {links_count} for selector 'Практичний іспит'.")
            return
        
        link_selector.click()
        logger.info("Practical exam link clicked successfully.")
    except Exception as e:
        logger.error(f"Failed to click the practical exam link: {e}")

def click_first_date_link(page):
    try:
        link_selector = page.locator('a.btn.btn-lg.icon-btn.btn-hsc-green.text-center').nth(0)
        link_selector.wait_for(state="visible")

        logger.info("Waiting for 2 seconds before clicking the link...")
        time.sleep(2)

        link_selector.click()
        logger.info("Successfully clicked the first date link.")
    except Exception as e:
        logger.error(f"Failed to click the first date link: {e}")

def click_and_check_talons(page):
    try:
        right_arrow_selector = 'i.fa.fa-arrow-circle-right.fa-2x'
        left_arrow_selector = 'i.fa.fa-arrow-circle-left.fa-2x'
        talon_icon_selector = 'img[src="/images/hsc_s.png"][style*="transform: translate3d(304px, 315px, 0px)"]'
        talon_present_selector = 'img[src="/images/hsc_i.png"]:first-child'
        
        right_click_count = 0
        left_click_count = 0
        
        while True:
            if right_click_count < 18:
                page.locator(right_arrow_selector).click()
                right_click_count += 1
                logger.info(f"Clicked the next button {right_click_count} times.")
            else:
                page.locator(left_arrow_selector).click()
                left_click_count += 1
                logger.info(f"Clicked the previous button {left_click_count} times.")
                
                if left_click_count == 18:
                    right_click_count = 0
                    left_click_count = 0

            talon_icon = page.locator(talon_icon_selector)
            talon_present = page.locator(talon_present_selector)
            
            if talon_present.is_visible():
                logger.info("Available talons found.")
                break

            logger.info("No talon found yet. Retrying in 2 seconds...")
            time.sleep(2)
    except Exception as e:
        logger.error(f"Error while clicking talons: {e}")
        raise
