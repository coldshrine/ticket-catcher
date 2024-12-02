import time
import logging
from playwright.sync_api import sync_playwright, TimeoutError
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


from constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def click_practical_exam_school_vehicle_button(page):
    try:
        button_selector = page.get_by_role("button", name="Практичний іспит (транспортний засіб навчального закладу)")
        
        buttons_count = button_selector.count()
        if buttons_count != 1:
            logger.error(f"Expected 1 button but found {buttons_count} for selector 'Практичний іспит (транспортний засіб навчального закладу)'.")
            return
        
        button_selector.click()
        logger.info("Practical exam school vehicle button clicked successfully.")
    except Exception as e:
        logger.error(f"Failed to click the practical exam school vehicle button: {e}")

def click_successful_theory_exam_button(page):
    try:
        button_selector = page.locator('button[data-target="#ModalCenter4"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")')
        button_selector.wait_for(state="visible")

        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)

        button_selector.click()
        logger.info("Successfully clicked the 'Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.' button.")
    except Exception as e:
        logger.error(f"Failed to click the 'Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.' button: {e}")

def click_successful_exam_button(page):
    try:
        button_selector = page.locator('button[data-target="#ModalCenter5"]:has-text("Так")')
        button_selector.wait_for(state="visible")

        logger.info("Waiting for 2 seconds before clicking the button...")
        time.sleep(2)

        button_selector.click()
        logger.info("Successfully clicked the 'Так' button.")
    except Exception as e:
        logger.error(f"Failed to click the 'Так' button: {e}")

def click_confirm_practical_exam_link(page):
    try:
        link_selector = page.locator('a[href="/site/step1"]:has-text("Практичний іспит на категорії B; BE")')
        link_selector.wait_for(state="visible")

        logger.info("Waiting for 2 seconds before clicking the link...")
        time.sleep(2)

        link_selector.click()
        logger.info("Successfully clicked the 'Практичний іспит на категорії B; BE' link.")
    except Exception as e:
        logger.error(f"Failed to click the 'Практичний іспит на категорії B; BE' link: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        open_login_page(page)
        select_checkbox(page)
        click_sign_up_button(page)
        click_electronic_signature_button(page)
        upload_file_jks(page, JKS_FILE_PATH_MAC)
        password = extract_jks_password(PASSWORD_FILE_PATH_MAC)
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
        logger.info("Browser session closed.")

if __name__ == "__main__":
    main()
