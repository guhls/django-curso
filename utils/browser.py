import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent

CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME

SELENIUM_HEADLESS = os.environ.get('SELENIUM_HEADLESS')

# Definir: options -> service -> browser


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if SELENIUM_HEADLESS == '1':
        chrome_options.add_argument('--headless')

    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser('--headless')
    browser.get('https://google.com.br/')
    sleep(3)
    browser.quit()
