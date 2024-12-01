"""
Automates interaction with the service center website using Playwright.
Includes functionality for login, button clicks, and form submissions.
"""

import time
import logging
from playwright.sync_api import sync_playwright
from constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC
from instructor_supervised import (
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
    """
    Clicks the 'Practical Exam Service Center Vehicle' button.

    Args:
        page: The Playwright page object.
    """
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
    except Exception as exc:  # noqa: W0703
        logger.error("Failed to click the practical exam service center vehicle button: %s", exc)


def service_center_click_successful_theory_exam_button(page):
    """
    Clicks the 'Successful Theory Exam' button.

    Args:
        page: The Playwright page object.
    """
    try:
        button_selector = page.locator(
            'button[data-target="#ModalCenterServiceCenter1"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")'
        )
        button_selector.wait_for(state="visible", timeout=5000)
        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)
        button_selector.click()
        logger.info("Successfully clicked the theory exam button.")
    except Exception as exc:  # noqa: W0703
        logger.error("Failed to click the theory exam button: %s", exc)


def service_center_click_successful_exam_button(page):
    """
    Clicks the 'Successful Exam' button.

    Args:
        page: The Playwright page object.
    """
    try:
        button_selector = page.locator(
            'a[href="/site/step_cs"]:has-text("Так")'
        )
        button_selector.wait_for(state="visible", timeout=5000)
        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)
        button_selector.click()
        logger.info("Successfully clicked the 'Так' button.")
    except Exception as exc:  # noqa: W0703
        logger.error("Failed to click the 'Так' button: %s", exc)


def service_center_click_confirm_practical_exam_link(page):
    """
    Clicks the 'Confirm Practical Exam' link.

    Args:
        page: The Playwright page object.
    """
    try:
        link_selector = page.locator(
            'a[href="/site/step1"]:has-text("Практичний іспит на категорію В (з механічною коробкою передач)")'
        )
        link_selector.wait_for(state="visible", timeout=5000)
        logger.info("Waiting for 2 seconds before clicking the link...")
        time.sleep(2)
        link_selector.click()
        logger.info("Successfully clicked the practical exam confirmation link.")
    except Exception as exc:  # noqa: W0703
        logger.error("Failed to click the practical exam confirmation link: %s", exc)


def main():
    """
    Main function to automate actions on the service center website.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        try:
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
        finally:
            browser.close()


if __name__ == "__main__":
    main()
