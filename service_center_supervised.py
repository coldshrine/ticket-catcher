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

# Configure logging
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

def main():
    with sync_playwright() as playwright:
        # Profile Path - Ensure it's properly referenced
        user_data_path = "/Users/caroline/Library/Application Support/Google/Chrome/Profile 1"
        extension_path = "/Users/caroline/Library/Application Support/Google/Chrome/Profile 1/Extensions/bbdhfoclddncoaomddgkaaphcnddbpdh/0.1.0_0"

        # Debugging step: Check if the profile folder exists
        if not os.path.exists(user_data_path):
            logger.error(f"Profile path {user_data_path} does not exist!")
            return
        if not os.path.exists(extension_path):
            logger.error(f"Extension path {extension_path} does not exist!")
            return
        logger.info(f"Using profile path: {user_data_path}")
        logger.info(f"Using extension path: {extension_path}")

        # Launch the browser with persistent context (this loads the profile and extension)
        try:
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_path,  # Use the correct profile path here
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # Path to Chrome executable
                headless=False,  # Run in non-headless mode to see the browser UI and extensions
                args=[
                    "--disable-infobars",  # Disable infobars
                    "--no-sandbox",  # Disable sandboxing (for debugging purposes)
                    "--disable-extensions-except=" + extension_path,  # Load specific extension
                ]
            )
            page = browser.new_page()

            # Disable automation flag to hide the automation flag
            page.evaluate('navigator.webdriver = false;')

            open_login_page(page)
            select_checkbox(page)
            click_sign_up_button(page)
            click_electronic_signature_button(page)
            upload_file_jks(page, JKS_FILE_PATH_MAC)
            password = extract_jks_password(PASSWORD_FILE_PATH_MAC)
            enter_password(page, password)
            zpysatys_button(page)
            select_practical_exam_link(page)
            click_practical_exam_service_center_vehicle_button(page)
            service_center_click_successful_theory_exam_button(page)
            service_center_click_successful_exam_button(page)
            service_center_click_confirm_practical_exam_link(page)
            click_first_date_link(page)
            click_and_check_talons(page)

        except Exception as exc:
            logger.error(f"Error during the browser session: {exc}")
        finally:
            # Always close the browser
            browser.close()

if __name__ == "__main__":
    main()