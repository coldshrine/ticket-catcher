import os
import time
from playwright.sync_api import sync_playwright, TimeoutError
from constants import JKS_FILE_PATH, PASSWORD_FILE_PATH
import subprocess

def simulate_file_picker(file_path):
    """
    Simulates navigation and selection in the file picker using xdotool.
    """
    folder_path = os.path.dirname(file_path)
    commands = [
        f'xdotool type "{folder_path}"',
        "xdotool key Return"
    ]
    for command in commands:
        time.sleep(1)
        subprocess.run(command, shell=True)

def open_login_page(page):
    try:
        page.goto("https://eq.hsc.gov.ua/")
        page.wait_for_load_state('domcontentloaded')
    except TimeoutError as e:
        print(f"Timeout while loading login page: {e}")
        raise

def select_checkbox(page):
    try:
        page.wait_for_selector('input[type="checkbox"]', timeout=5000)
        checkbox = page.locator('input[type="checkbox"]')
        checkbox.click()
    except TimeoutError as e:
        print(f"Timeout while selecting checkbox: {e}")
        raise

def click_sign_up_button(page):
    page.wait_for_selector('a.btn.btn-lg.btn-hsc-green_s')
    button = page.locator('a.btn.btn-lg.btn-hsc-green_s')
    button.click()
    page.wait_for_load_state('networkidle')

def click_electronic_signature_button(page):
    try:
        page.wait_for_selector('a.a1', timeout=5000)
        sign_button = page.locator('a.a1', has_text="Електронного підпису")
        sign_button.click()
        page.wait_for_load_state('networkidle')
    except TimeoutError as e:
        print(f"Timeout while clicking electronic signature button: {e}")
        raise

def upload_jks_file(page, file_path):
    try:
        page.wait_for_selector('span:has-text("оберіть його на своєму носієві")', timeout=20000)
        page.locator('span:has-text("оберіть його на своєму носієві")').click()
        simulate_file_picker(file_path)
        print(f"Successfully uploaded the file: {file_path}")
    except Exception as e:
        print(f"Failed to upload the file due to: {e}")
        raise

def extract_password(file_path):
    try:
        with open(file_path, 'r') as file:
            password = file.read().strip()
        return password
    except FileNotFoundError:
        print(f"Password file not found at {file_path}")
        raise
    except Exception as e:
        print(f"Error while reading password file: {e}")
        raise

import time

def enter_password(page, password):
    """
    Enters the password into the input field without clicking 'Продовжити'.
    """
    try:
        page.wait_for_selector('#PKeyPassword', timeout=5000)
        page.wait_for_function('document.querySelector("#PKeyPassword").offsetHeight > 0 && document.querySelector("#PKeyPassword").offsetWidth > 0')
        is_visible = page.is_visible('#PKeyPassword')
        is_enabled = page.is_enabled('#PKeyPassword')
        print(f"Password input field visible: {is_visible}, enabled: {is_enabled}")

        if not is_visible or not is_enabled:
            print("Password input field is either not visible or not enabled.")
            return
        time.sleep(1)
        
        page.fill('#PKeyPassword', password)
        print(f"Password entered successfully: {password}")
        
    except Exception as e:
        print(f"An error occurred while entering the password: {e}")
        raise



def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        open_login_page(page)
        select_checkbox(page)
        click_sign_up_button(page)
        click_electronic_signature_button(page)
        upload_jks_file(page, JKS_FILE_PATH)
        password = extract_password(PASSWORD_FILE_PATH)
        print(password)
        enter_password(page, password)
        time.sleep(20)
        browser.close()

if __name__ == "__main__":
    main()
