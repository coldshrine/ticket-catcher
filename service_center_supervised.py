import time
import logging
import os
from playwright.sync_api import sync_playwright
from constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC
from common_login import (
    open_login_page,
    select_checkbox,
    click_sign_up_button,
    click_electronic_signature_button,
    upload_file_jks,
    extract_jks_password,
    enter_password,
    zpysatys_button,
    select_practical_exam_link,
    click_first_date_link,
    click_and_check_talons,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def click_practical_exam_service_center_vehicle_button(page):
    try:
        button_selector = page.locator(
            'button.btn.btn-lg.icon-btn.btn-hsc-green_:has-text("Практичний іспит (транспортний засіб сервісного центру)")'
        )
        buttons_count = button_selector.count()
        if buttons_count != 1:
            logger.error(
                "Expected 1 button but found %s for the selector.",
                buttons_count,
            )
            return
        button_selector.click()
        logger.info("Practical exam service center vehicle button clicked successfully.")
    except Exception as exc:
        logger.error("Failed to click the practical exam service center vehicle button: %s", exc)

def service_center_click_successful_theory_exam_button(page):
    try:
        button_selector = page.locator(
            'button[data-target="#ModalCenterServiceCenter1"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")'
        )
        button_selector.wait_for(state="visible", timeout=15000)
        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)
        button_selector.click()
        logger.info("Successfully clicked the theory exam button.")
    except Exception as exc:
        logger.error("Failed to click the theory exam button: %s", exc)

def service_center_click_successful_exam_button(page):
    try:
        button_selector = page.locator(
            'a[href="/site/step_cs"]:has-text("Так")'
        )
        button_selector.wait_for(state="visible", timeout=15000)
        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)
        button_selector.click()
        logger.info("Successfully clicked the 'Так' button.")
    except Exception as exc:
        logger.error("Failed to click the 'Так' button: %s", exc)

def service_center_click_confirm_practical_exam_link(page):
    try:
        link_selector = page.locator(
            'a[href="/site/step1"]:has-text("Практичний іспит на категорію В (з механічною коробкою передач)")'
        )
        link_selector.wait_for(state="visible", timeout=15000)
        logger.info("Waiting for 2 seconds before clicking the link...")
        time.sleep(2)
        link_selector.click()
        logger.info("Successfully clicked the practical exam confirmation link.")
    except Exception as exc:
        logger.error("Failed to click the practical exam confirmation link: %s", exc)

def pass_recaptcha(page, target_url="https://eq.hsc.gov.ua/site/recaptcha", wait_time=20):
    try:
        logger.info(f"Current URL: {page.url}")  # Log the current URL
        if page.url == target_url:  # Check if the current page is the reCAPTCHA page
            logger.info(f"Waiting for page to navigate to {target_url}...")
            page.wait_for_url(target_url, timeout=60000)  # Wait for the reCAPTCHA page
            logger.info(f"Page navigated to {target_url}. Giving user {wait_time} seconds to pass reCAPTCHA...")
            
            recaptcha_button_selector = page.locator('button.btn.btn-warning:has-text("Підтвердити")')
            logger.info(f"Locator found: {recaptcha_button_selector}")
            
            recaptcha_button_selector.wait_for(state="visible", timeout=30000)  # Wait for the button
            recaptcha_button_selector.wait_for(state="enabled", timeout=30000)  # Ensure the button is enabled
            
            logger.info("reCAPTCHA button is now enabled and ready to be clicked.")
            recaptcha_button_selector.click()
            logger.info("Successfully clicked the 'Підтвердити' button.")
        else:
            logger.error("Not on the reCAPTCHA page. Current URL: %s", page.url)
    except Exception as exc:
        logger.error(f"Failed to handle reCAPTCHA page: {exc}")

def perform_action_with_recaptcha_check(page, action, *args, **kwargs):
    try:
        # Check if the reCAPTCHA page is loaded before performing the action
        if "recaptcha" in page.url:
            pass_recaptcha(page)  # Ensure reCAPTCHA is passed before proceeding
        
        action(page, *args, **kwargs)
    except Exception as exc:
        logger.error(f"Failed to execute action with reCAPTCHA check: {exc}")

def main():
    with sync_playwright() as playwright:
        user_data_path = "/Users/caroline/Library/Application Support/Google/Chrome/Profile 1"
        extension_path = "/Users/caroline/Library/Application Support/Google/Chrome/Profile 1/Extensions/bbdhfoclddncoaomddgkaaphcnddbpdh/0.1.0_0"

        if not os.path.exists(user_data_path):
            logger.error(f"Profile path {user_data_path} does not exist!")
            return
        if not os.path.exists(extension_path):
            logger.error(f"Extension path {extension_path} does not exist!")
            return
        logger.info(f"Using profile path: {user_data_path}")
        logger.info(f"Using extension path: {extension_path}")

        try:
            # Launch the browser
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_path,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", 
                headless=False,
                args=[
                    "--disable-infobars",
                    "--no-sandbox",
                    "--disable-extensions-except=" + extension_path,
                ]
            )

            # Get all open pages (no need for parentheses)
            pages = browser.pages

            logger.info(f"Number of pages open: {len(pages)}")

            # If no pages are open, log and return
            if len(pages) == 0:
                logger.error("No pages are open. Exiting...")
                return

            # Debug: Log the URL of the first page
            page = pages[0]
            logger.info(f"First page URL: {page.url}")

            # Trigger the loading of the page (if not already done)
            # For example, navigating to a specific URL
            page.goto("https://eq.hsc.gov.ua/")  # Replace with your target URL

            # Wait for the page to load completely
            logger.info("Waiting for the page to load...")
            page.wait_for_load_state("domcontentloaded")  # Wait until the DOM is fully loaded

            # Wait a bit to ensure everything has loaded (additional safety)
            page.wait_for_timeout(3000)  # Optional: you can wait an additional 3 seconds

            # Debug: Log the current URL after page load
            logger.info(f"Current page URL after wait: {page.url}")

            # Now check if reCAPTCHA is detected
            if "recaptcha" in page.url or page.locator('iframe[src*="recaptcha"]').is_visible():
                logger.info("reCAPTCHA detected. Attempting to pass it...")
                pass_recaptcha(page)
            else:
                logger.info("No reCAPTCHA detected, proceeding with login.")

            # Proceed with login actions if no reCAPTCHA or after handling it
            open_login_page(page)
            select_checkbox(page)
            click_sign_up_button(page)
            click_electronic_signature_button(page)
            upload_file_jks(page, JKS_FILE_PATH_MAC)
            password = extract_jks_password(PASSWORD_FILE_PATH_MAC)
            enter_password(page, password)
            zpysatys_button(page)
            select_practical_exam_link(page)

            # Perform further actions
            perform_action_with_recaptcha_check(page, click_practical_exam_service_center_vehicle_button)
            perform_action_with_recaptcha_check(page, service_center_click_successful_theory_exam_button)
            perform_action_with_recaptcha_check(page, service_center_click_successful_exam_button)
            perform_action_with_recaptcha_check(page, service_center_click_confirm_practical_exam_link)
            perform_action_with_recaptcha_check(page, click_first_date_link)
            perform_action_with_recaptcha_check(page, click_and_check_talons)

        except Exception as exc:
            logger.error(f"Error during the browser session: {exc}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()