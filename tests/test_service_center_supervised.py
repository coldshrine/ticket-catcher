import time
import logging
from playwright.sync_api import sync_playwright, TimeoutError
from test_constants import PASSWORD_FILE_PATH_MAC, JKS_FILE_PATH_MAC
from test_instructor_supervised import (
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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PlaywrightActions:
    @staticmethod
    def click_button(page, selector: str, button_name: str, retry_count: int = 3) -> bool:
        """Clicks a button and retries if the action fails."""
        try:
            for attempt in range(retry_count):
                try:
                    button = page.locator(selector)
                    button.wait_for(state="visible", timeout=5000)
                    button.click()
                    logger.info(f"'{button_name}' button clicked successfully.")
                    return True
                except TimeoutError:
                    logger.warning(f"Attempt {attempt + 1}: '{button_name}' button not visible.")
                except Exception as e:
                    logger.error(f"Error while clicking '{button_name}' button: {e}")
            return False
        except Exception as e:
            logger.error(f"Unhandled error in clicking '{button_name}' button: {e}")
            return False

    @staticmethod
    def click_link(page, selector: str, link_name: str, retry_count: int = 3) -> bool:
        """Clicks a link and retries if the action fails."""
        try:
            for attempt in range(retry_count):
                try:
                    link = page.locator(selector)
                    link.wait_for(state="visible", timeout=5000)
                    link.click()
                    logger.info(f"'{link_name}' link clicked successfully.")
                    return True
                except TimeoutError:
                    logger.warning(f"Attempt {attempt + 1}: '{link_name}' link not visible.")
                except Exception as e:
                    logger.error(f"Error while clicking '{link_name}' link: {e}")
            return False
        except Exception as e:
            logger.error(f"Unhandled error in clicking '{link_name}' link: {e}")
            return False

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            open_login_page(page)
            select_checkbox(page)
            click_sign_up_button(page)
            click_electronic_signature_button(page)
            upload_file_jks(page, JKS_FILE_PATH_MAC)

            try:
                password = extract_jks_password(PASSWORD_FILE_PATH_MAC)
            except FileNotFoundError as e:
                logger.error(f"Password file not found: {e}")
                return

            enter_password(page, password)
            zpysatys_button(page)
            select_practical_exam_link(page)

            PlaywrightActions.click_button(
                page,
                'button.btn.btn-lg.icon-btn.btn-hsc-green_:has-text("Практичний іспит (транспортний засіб сервісного центру)")',
                "Practical Exam Service Center Vehicle"
            )

            PlaywrightActions.click_button(
                page,
                'button[data-target="#ModalCenterServiceCenter1"]:has-text("Так. Я успішно склав теоретичний іспит в сервісному центрі МВС.")',
                "Successful Theory Exam Confirmation"
            )

            PlaywrightActions.click_button(
                page,
                'a[href="/site/step_cs"]:has-text("Так")',
                "Successful Exam Confirmation"
            )

            PlaywrightActions.click_link(
                page,
                'a[href="/site/step1"]:has-text("Практичний іспит на категорію В (з механічною коробкою передач)")',
                "Practical Exam Confirmation Link"
            )

            click_first_date_link(page)
            click_and_check_talons(page)

        except Exception as e:
            logger.error(f"Unhandled error in the main workflow: {e}")
        finally:
            browser.close()
            logger.info("Browser session closed.")

if __name__ == "__main__":
    main()
