from playwright.sync_api import sync_playwright, TimeoutError
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def car_of_driving_school_picker(page):
    """
    Clicks the 'Записатись' button to proceed to the next step.
    
    Args:
    - page: The Playwright page object.
    """
    try:
        # Wait for the button to appear and be interactable
        page.wait_for_selector('button.btn.bt-xs.btn-hsc-green_s', timeout=5000)
        
        # Locate and click the button
        page.locator('button.btn.bt-xs.btn-hsc-green_s').click()
        
        # Wait for the page to finish navigation
        page.wait_for_load_state('networkidle')
        logger.info("Sign-up button clicked successfully.")
    except TimeoutError:
        logger.error("Timeout while waiting for the 'Записатись' button.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise

def main():
    """
    Main function to handle running the car_of_driving_school_picker after login.
    """
    # Run the login script as a subprocess
    subprocess.run(["python", "login_2fa.py"])
    logger.info("login_2fa.py executed successfully.")


    car_of_driving_school_picker(page)

if __name__ == "__main__":
    main()
