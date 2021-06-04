import sys
import os
from Parser import AddressParser
from time import sleep
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")
options.binary_location = r"/usr/bin/google-chrome-stable"
executable_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"

USERNAME = 'geoorbital'

def main():

    # for personal use
    with open('pass.txt') as f:
        pswd = f.read().strip()

    assert len(sys.argv) <= 2
    addr_file = sys.argv[1:]
    if addr_file:
        addr_file, = addr_file
    else:
        addr_file = None

    parser = AddressParser(addr_file)
    parser.dump()

    with webdriver.Chrome(executable_path=executable_path, options=options) as driver:
        # login to Github
        driver.get('https://www.fedex.com/en-us/home.html')

        driver.find_element_by_id('fxg-dropdown-signIn').click()

        username_field = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.NAME, 'user'))).send_keys('geoorbital')

        password_field = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.NAME, 'pwd'))).send_keys(pswd)

        driver.find_element_by_xpath('/html/body/div[1]/header/div/div/nav/div/div/div/div[1]/div/div/form/button').click()

        sleep(20)
        exit()

if __name__ == "__main__":
    main()
