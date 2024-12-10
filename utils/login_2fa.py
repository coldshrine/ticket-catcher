import os
import time
import logging
from playwright.sync_api import sync_playwright, TimeoutError
import subprocess

from utils.constants import JKS_FILE_PATH, PASSWORD_FILE_PATH


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simulate_file_picker(file_path: str) -> None:
    """
    Simulates interaction with a file picker by typing the folder path
    of the provided file and simulating a 'Return' key press.

    Args:
        file_path (str): The full path to the file for which the folder path
                         is used in the simulated file picker.
    """
    folder_path: str = os.path.dirname(file_path)
    commands: List[str] = [
        f'xdotool type "{folder_path}"',
        "xdotool key Return"
    ]
    for command in commands:
        time.sleep(1)
        subprocess.run(command, shell=True)
    logger.info(f"Simulated file picker for file: {file_path}")


def open_login_page(page: Page) -> None:
    """
    Opens the login page and waits for it to load completely.

    Args:
        page (Page): A Playwright Page object used to interact with the browser.

    Raises:
        TimeoutError: If the page fails to load within the timeout period.
    """
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


def zpysatys_button(page):
    try:
        # Use a more specific selector to target the correct button
        button_selector = page.get_by_role("button", name="Записатись")
        
        # Ensure the button exists and log the count of matching elements
        buttons_count = button_selector.count()
        if buttons_count != 1:
            logger.error(f"Expected 1 button but found {buttons_count} for selector 'Записатись'.")
            return
        
        # Click the button
        button_selector.click()
        logger.info("Sign-up button clicked successfully.")
    except Exception as e:
        logger.error(f"Failed to click the sign-up button: {e}")

def select_practical_exam_link(page):

    try:
        # Use a specific selector to target the "Практичний іспит" link
        link_selector = page.get_by_role("link", name="Практичний іспит")
        
        # Ensure the link exists and log the count of matching elements
        links_count = link_selector.count()
        if links_count != 1:
            logger.error(f"Expected 1 link but found {links_count} for selector 'Практичний іспит'.")
            return
        
        # Click the link
        link_selector.click()
        logger.info("Practical exam link clicked successfully.")
    except Exception as e:
        logger.error(f"Failed to click the practical exam link: {e}")


def click_practical_exam_school_vehicle_button(page):

    try:
        # Use a specific selector to locate the button by its text
        button_selector = page.get_by_role("button", name="Практичний іспит (транспортний засіб навчального закладу)")
        
        # Ensure the button exists and log the count of matching elements
        buttons_count = button_selector.count()
        if buttons_count != 1:
            logger.error(f"Expected 1 button but found {buttons_count} for selector 'Практичний іспит (транспортний засіб навчального закладу)'.")
            return
        
        # Click the button
        button_selector.click()
        logger.info("Practical exam school vehicle button clicked successfully.")
    except Exception as e:
        logger.error(f"Failed to click the practical exam school vehicle button: {e}")

def click_successful_theory_exam_button(page):

    try:
        # Locate the button using both 'data-target' and the text of the button
        button_selector = page.locator('button[data-target="#ModalCenter4"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")')

        # Wait for the button to be visible (optional)
        button_selector.wait_for(state="visible")

        # Wait for 2 seconds
        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)

        # Click the button
        button_selector.click()
        logger.info("Successfully clicked the 'Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.' button.")
    except Exception as e:
        logger.error(f"Failed to click the 'Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.' button: {e}")

def click_successful_exam_button(page):

    try:
        # Locate the button using 'data-target' and the text of the button
        button_selector = page.locator('button[data-target="#ModalCenter5"]:has-text("Так")')

        # Wait for the button to be visible (optional)
        button_selector.wait_for(state="visible")

        # Wait for 2 seconds before clicking
        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)

        # Click the button
        button_selector.click()
        logger.info("Successfully clicked the 'Так' button.")
    except Exception as e:
        logger.error(f"Failed to click the 'Так' button: {e}")

def click_confirm_practical_exam_link(page):

    try:
        # Locate the link by its href and visible text
        link_selector = page.locator('a[href="/site/step1"]:has-text("Практичний іспит на категорії B; BE")')

        # Wait for the link to be visible
        link_selector.wait_for(state="visible")

        # Wait for 2 seconds before clicking
        logger.info("Waiting for 2 seconds before clicking the link...")
        time.sleep(2)

        # Click the link
        link_selector.click()
        logger.info("Successfully clicked the 'Практичний іспит на категорії B; BE' link.")
    except Exception as e:
        logger.error(f"Failed to click the 'Практичний іспит на категорії B; BE' link: {e}")

def click_first_date_link(page):

    try:
        # Locate the first anchor tag with the specified class, regardless of the date text
        link_selector = page.locator('a.btn.btn-lg.icon-btn.btn-hsc-green.text-center').nth(0)

        # Wait for the link to be visible
        link_selector.wait_for(state="visible")

        # Wait for 2 seconds before clicking
        logger.info("Waiting for 2 seconds before clicking the link...")
        time.sleep(2)

        # Click the first link
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
        
        # Counter for the clicks
        right_click_count = 0
        left_click_count = 0
        
        while True:
            if right_click_count < 20:
                page.locator(right_arrow_selector).click()
                right_click_count += 1
                logger.info(f"Clicked the next button {right_click_count} times.")
            else:
                # After 20 right clicks, switch to left arrow clicks
                page.locator(left_arrow_selector).click()
                left_click_count += 1
                logger.info(f"Clicked the previous button {left_click_count} times.")
                
                # Reset right click count after switching to left
                if left_click_count == 20:
                    right_click_count = 0
                    left_click_count = 0

            # Wait for talon icon to appear
            talon_icon = page.locator(talon_icon_selector)
            talon_icon.wait_for(state="visible")
        
            talon_icon.first.hover()
            logger.info("Hovered over the talon icon.")

            talon_present = page.locator(talon_present_selector).is_visible()

            if talon_present:
                print("є талони на сайті м. Івано-Франківськ, вул. Є Коновальця 229")
            else:
                print("немає талонів")
            
            time.sleep(1)

    except Exception as e:
        logger.error(f"Error during talon check process: {e}")

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
        zpysatys_button(page)
        select_practical_exam_link(page)
        click_practical_exam_school_vehicle_button(page)
        click_successful_theory_exam_button(page)
        click_successful_exam_button(page)
        click_confirm_practical_exam_link(page)
        click_first_date_link(page)
        click_and_check_talons(page)
        time.sleep(60000)
        logger.info("Browser session closed.")

if __name__ == "__main__":
    main()
