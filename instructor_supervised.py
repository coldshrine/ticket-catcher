import time
import logging
from playwright.sync_api import sync_playwright, Playwright, Browser, Page, Locator, TimeoutError
from typing import Tuple, Optional
from utils.common_login import (
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
from utils.constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def setup_browser() -> Tuple[Playwright, Browser, Page]:
    """Sets up the browser and page for testing."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    return playwright, browser, page


def click_practical_exam_school_vehicle_button(page: Page) -> None:
    """Clicks the button for the practical exam with a school vehicle."""
    try:
        button_selector: Locator = page.get_by_role("button", name="Практичний іспит (транспортний засіб навчального закладу)")
        if button_selector.count() == 1:
            button_selector.click()
            logger.info("Clicked 'Практичний іспит (транспортний засіб навчального закладу)' button.")
        else:
            logger.error("Expected 1 button but found multiple.")
    except Exception as e:
        logger.error(f"Error clicking 'Практичний іспит (транспортний засіб навчального закладу)' button: {e}")


def click_successful_theory_exam_button(page: Page) -> None:
    """Clicks the button confirming successful theory exam."""
    try:
        button_selector: Locator = page.locator(
            'button[data-target="#ModalCenter4"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")'
        )
        button_selector.wait_for(state="visible")
        time.sleep(2)
        button_selector.click()
        logger.info("Clicked 'Так. Я успішно склав теоретичний іспит...' button.")
    except Exception as e:
        logger.error(f"Error clicking theory exam confirmation button: {e}")


def click_successful_exam_button(page: Page) -> None:
    """Clicks the general 'Так' confirmation button."""
    try:
        button_selector: Locator = page.locator('button[data-target="#ModalCenter5"]:has-text("Так")')
        button_selector.wait_for(state="visible")
        time.sleep(2)
        button_selector.click()
        logger.info("Clicked 'Так' button.")
    except Exception as e:
        logger.error(f"Error clicking 'Так' button: {e}")


def click_confirm_practical_exam_link(page: Page) -> None:
    """Clicks the practical exam confirmation link."""
    try:
        link_selector: Locator = page.locator('a[href="/site/step1"]:has-text("Практичний іспит на категорії B; BE")')
        link_selector.wait_for(state="visible")
        time.sleep(2)
        link_selector.click()
        logger.info("Clicked 'Практичний іспит на категорії B; BE' link.")
    except Exception as e:
        logger.error(f"Error clicking practical exam confirmation link: {e}")


def main() -> None:
    playwright: Optional[Playwright] = None
    browser: Optional[Browser] = None
    page: Optional[Page] = None
    try:
        playwright, browser, page = setup_browser()
        open_login_page(page)
        select_checkbox(page)
        click_sign_up_button(page)
        click_electronic_signature_button(page)
        upload_file_jks(page, JKS_FILE_PATH_MAC)
        password: str = extract_jks_password(PASSWORD_FILE_PATH_MAC)
        logger.info("Password successfully extracted.")
        enter_password(page, password)
        zpysatys_button(page)
        select_practical_exam_link(page)
        click_practical_exam_school_vehicle_button(page)
        click_successful_theory_exam_button(page)
        click_successful_exam_button(page)
        click_confirm_practical_exam_link(page)
        click_first_date_link(page)
        click_and_check_talons(page)
    except Exception as e:
        logger.error(f"An error occurred during the main execution: {e}")
    finally:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()


if __name__ == "__main__":
    main()
