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

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Functions to interact with elements
def click_practical_exam_service_center_vehicle_button(page):
    try:
        button_selector = page.locator(
            'button.btn.btn-lg.icon-btn.btn-hsc-green_:has-text("Практичний іспит (транспортний засіб сервісного центру)")'
        )
        if button_selector.count() == 1:
            button_selector.click()
            logger.info("Practical exam service center vehicle button clicked successfully.")
        else:
            logger.error("Expected 1 button but found %d buttons.", button_selector.count())
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

def pass_recaptcha(page, wait_time=20):
    try:
        logger.info(f"Current URL: {page.url}")
        # Wait for any reCAPTCHA-related element to appear
        recaptcha_frame = page.locator('iframe[src*="recaptcha"]')
        recaptcha_frame.wait_for(state="attached", timeout=60000)
        
        logger.info("reCAPTCHA frame detected. Waiting for user interaction...")
        # Here you might want to pause the script for manual interaction or use a solver
        time.sleep(wait_time)  # Pause to give the user time to solve the CAPTCHA manually
        
        # Continue after reCAPTCHA is solved
        page.wait_for_url(lambda url: url != page.url, timeout=60000)
        logger.info("Successfully navigated away from the reCAPTCHA page.")
    except Exception as exc:
        logger.error(f"Failed to handle reCAPTCHA: {exc}")


def perform_action_with_recaptcha_check(page, action, *args, **kwargs):
    try:
        if "recaptcha" in page.url:
            logger.info("Detected reCAPTCHA page. Handling reCAPTCHA before proceeding.")
            pass_recaptcha(page)  # Ensure reCAPTCHA is passed before proceeding
        
        logger.info("Executing action after passing reCAPTCHA.")
        action(page, *args, **kwargs)
    except Exception as exc:
        logger.error(f"Failed to execute action with reCAPTCHA check: {exc}")

# Main function
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

            page = browser.new_page()
            page.goto('https://eq.hsc.gov.ua/site/step')

            service_selection_header = page.locator('h3.align-middle.align-content-center:has-text("Оберіть послугу")')
            service_selection_header.wait_for(state="visible", timeout=90000)

            if service_selection_header.is_visible():
                logger.info("Service selection page loaded. Proceeding with further actions.")
                
                perform_action_with_recaptcha_check(page, select_practical_exam_link)
                perform_action_with_recaptcha_check(page, click_practical_exam_service_center_vehicle_button)
                perform_action_with_recaptcha_check(page, service_center_click_successful_theory_exam_button)
                perform_action_with_recaptcha_check(page, service_center_click_successful_exam_button)
                perform_action_with_recaptcha_check(page, service_center_click_confirm_practical_exam_link)
                perform_action_with_recaptcha_check(page, click_first_date_link)
                perform_action_with_recaptcha_check(page, click_and_check_talons)
            else:
                logger.error("Service selection page not loaded properly.")
                
        except Exception as exc:
            logger.error(f"Error during the browser session: {exc}")
        finally:
            browser.close()

if __name__ == "__main__":
    main()