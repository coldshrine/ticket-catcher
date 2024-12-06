JKS_FILE_PATH_MAC = "/Users/caroline/Desktop/ticket-catcher/user_files/mine.jks"
PASSWORD_FILE_PATH_MAC = "/Users/caroline/Desktop/ticket-catcher/user_files/password_for_jks.txt"

SELECTORS = {
    "checkbox": 'input[type="checkbox"]',
    "sign_up_button": 'a.btn.btn-lg.btn-hsc-green_s',
    "electronic_signature": 'a.a1:has-text("Електронного підпису")',
    "password_field": '#PKeyPassword',
    "continue_button": 'span.jss177:has-text("Продовжити")',
    "signup_button": 'button:has-text("Записатись")',
    "practical_exam_link": 'a:has-text("Практичний іспит")',
    "first_date_button": 'a.btn.btn-lg.icon-btn.btn-hsc-green.text-center',
    "right_arrow": 'i.fa.fa-arrow-circle-right.fa-2x',
    "left_arrow": 'i.fa.fa-arrow-circle-left.fa-2x',
    "talon_icon": 'img[src="/images/hsc_s.png"][style*="transform: translate3d(304px, 315px, 0px)"]',
    "talon_present": 'img[src="/images/hsc_i.png"]:first-child',
}


DEFAULT_TIMEOUT = 15000
RECAPTCHA_WAIT_TIME = 20

USER_DATA_PATH = "/Users/caroline/Library/Application Support/Google/Chrome/Profile 1"
EXTENSION_DATA_PATH = "/Users/caroline/Library/Application Support/Google/Chrome/Profile 1/Extensions/bbdhfoclddncoaomddgkaaphcnddbpdh/0.1.0_0"
