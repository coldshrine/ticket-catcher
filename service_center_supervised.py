import time
import logging
import os
from playwright.sync_api import sync_playwright
from constants import DEFAULT_TIMEOUT,RECAPTCHA_WAIT_TIME, USER_DATA_PATH, EXTENSION_DATA_PATH
from common_login import (
    select_practical_exam_link,
    click_first_date_link,
    click_and_check_talons,
)


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def safe_click(locator, description, timeout=DEFAULT_TIMEOUT):
    """Helper function to wait for and click an element."""
    try:
        locator.wait_for(state="visible", timeout=timeout)
        logger.info(f"Waiting for 2 seconds before clicking '{description}'...")
        time.sleep(2)
        locator.click()
        logger.info(f"Successfully clicked '{description}'.")
    except Exception as exc:
        logger.error(f"Failed to click '{description}': {exc}")

def pass_recaptcha(page, wait_time=RECAPTCHA_WAIT_TIME):
    """Handle reCAPTCHA manually or with a solver."""
    try:
        logger.info(f"Current URL: {page.url}")
        recaptcha_frame = page.locator('iframe[src*="recaptcha"]')
        recaptcha_frame.wait_for(state="attached", timeout=60000)
        logger.info("reCAPTCHA detected. Waiting for manual resolution...")
        time.sleep(wait_time)
        page.wait_for_url(lambda url: url != page.url, timeout=60000)
        logger.info("Successfully navigated away from the reCAPTCHA page.")
    except Exception as exc:
        logger.error(f"Failed to handle reCAPTCHA: {exc}")

def perform_action_with_recaptcha_check(page, action, *args, **kwargs):
    """Execute an action, ensuring reCAPTCHA is resolved first if necessary."""
    try:
        if "recaptcha" in page.url:
            logger.info("Detected reCAPTCHA. Attempting to resolve before proceeding.")
            pass_recaptcha(page)
        logger.info("Executing action after reCAPTCHA resolution.")
        action(page, *args, **kwargs)
    except Exception as exc:
        logger.error(f"Failed to execute action '{action.__name__}': {exc}")

def validate_paths(*paths):
    """Validate that provided paths exist."""
    for path in paths:
        if not os.path.exists(path):
            logger.error(f"Path does not exist: {path}")
            return False
    return True

def main():
    with sync_playwright() as playwright:

        if not validate_paths(USER_DATA_PATH, EXTENSION_DATA_PATH):
            return

        logger.info(f"Using profile path: {USER_DATA_PATH}")
        logger.info(f"Using extension path: {EXTENSION_DATA_PATH}")

        try:
            browser = playwright.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_PATH,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                headless=False,
                args=[
                    "--disable-infobars",
                    "--no-sandbox",
                    f"--disable-extensions-except={EXTENSION_DATA_PATH}",
                ],
            )

            page = browser.new_page()
            page.goto("https://eq.hsc.gov.ua/site/step")

            service_selection_header = page.locator(
                'h3.align-middle.align-content-center:has-text("Оберіть послугу")'
            )
            service_selection_header.wait_for(state="visible", timeout=DEFAULT_TIMEOUT)

            if service_selection_header.is_visible():
                logger.info("Service selection page loaded. Proceeding with further actions.")

                perform_action_with_recaptcha_check(page, select_practical_exam_link)
                perform_action_with_recaptcha_check(
                    page,
                    safe_click,
                    page.locator(
                        'button.btn.btn-lg.icon-btn.btn-hsc-green_:has-text("Практичний іспит (транспортний засіб сервісного центру)")'
                    ),
                    "Practical exam service center vehicle button",
                )
                perform_action_with_recaptcha_check(
                    page,
                    safe_click,
                    page.locator(
                        'button[data-target="#ModalCenterServiceCenter1"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")'
                    ),
                    "Theory exam button",
                )
                perform_action_with_recaptcha_check(
                    page,
                    safe_click,
                    page.locator('a[href="/site/step_cs"]:has-text("Так")'),
                    "Successful exam button",
                )
                perform_action_with_recaptcha_check(
                    page,
                    safe_click,
                    page.locator(
                        'a[href="/site/step1"]:has-text("Практичний іспит на категорію В (з механічною коробкою передач)")'
                    ),
                    "Practical exam confirmation link",
                )
                perform_action_with_recaptcha_check(page, click_first_date_link)
                perform_action_with_recaptcha_check(page, click_and_check_talons)
            else:
                logger.error("Service selection page not loaded properly.")
        except Exception as exc:
            logger.error(f"Error during the browser session: {exc}")
        finally:
            browser.close()
            logger.info("Browser session closed.")

if __name__ == "__main__":
    main()
