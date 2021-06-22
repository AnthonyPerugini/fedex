import sys
import os
import urllib.request
from Parser import AddressParser
from time import sleep
import datetime
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1600,900")
options.binary_location = r"/usr/bin/google-chrome-stable"

executable_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"

def main():

    # personal creds
    with open('pass.txt') as f:
        username, pswd = f.read().split()

    assert len(sys.argv) <= 2
    addr_file = sys.argv[1:]
    if addr_file:
        addr_file, = addr_file
    else:
        addr_file = None

    parser = AddressParser(addr_file)

    opt = input('0 for wheel, 1 for battery, 2 for charger: ')
    length, width, height = {'0': [28 ,28 ,8], '1': [8, 8, 16], '2': [6, 9, 2]}[opt]
    weight = input('weight: ')

    print('confirm parameters below:\n--------')
    parser.dump()
    print('Length, Width, Height: ', length, '" x ', width, '" x ', height, '"', sep='')
    print('Weight: ', weight, 'lbs')
    print('--------')
    if input('[y]/n?: ') == 'n':
        exit()

    with webdriver.Chrome(executable_path=executable_path, options=options) as driver:

        # Login to FedEx
        driver.get('https://www.fedex.com/en-us/home.html')

        driver.find_element_by_id('fxg-dropdown-signIn').click()

        count = 0

        while driver.find_element_by_xpath('//*[@id="fxg-dropdown-signIn"]/span').text == 'Sign Up or Log In' and count < 5:

            username_field = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.NAME, 'user')))

            username_field.send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
            username_field.send_keys(username)

            password_field = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.NAME, 'pwd')))

            password_field.send_keys(Keys.CONTROL, 'a', Keys.BACKSPACE)
            password_field.send_keys(pswd)

            driver.find_element_by_xpath('/html/body/div[1]/header/div/div/nav/div/div/div/div[1]/div/div/form/button').click()
            sleep(1)
            count += 1
        
        if count == 5:
            print('failed to login')
            input()
            exit()

        # Open shipping tab
        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div/nav/div/ul/div[1]/li/a/span'))).click()

        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, 
                            '/html/body/div[1]/header/div/div/nav/div/ul/div[1]/li/div/div[1]/div/a'))).click()

        # input shipping details
        def input_field_by_xpath(xpath, parser_attr):
            name_field = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, 
                                xpath)))
            # clear field
            name_field.send_keys(Keys.CONTROL, 'a')
            name_field.send_keys(Keys.BACK_SPACE)

            # fill field
            name_field.send_keys(parser_attr)
        
        input_field_by_xpath('//*[@id="toData.contactName"]', parser.name)
        input_field_by_xpath('//*[@id="toData.addressLine1"]', parser.address)
        input_field_by_xpath('//*[@id="toData.zipPostalCode"]', parser.zip)
        input_field_by_xpath('//*[@id="toData.city"]', parser.town)
        state_input = Select(driver.find_element_by_xpath('//*[@id="toData.stateProvinceCode"]'))
        state_input.select_by_value(parser.state)

        # TODO: phone number sometimes doesn't input correctly.  Need to figure out why
        sleep(.5)
        input_field_by_xpath('//*[@id="toData.phoneNumber"]', '9785059671')
        sleep(.5)
        driver.find_element_by_xpath('//*[@id="toData.phoneNumberExt"]').click()

        if parser.address2:
            input_field_by_xpath('//*[@id="toData.addressLine2"]', parser.address2)

        shipment_type = Select(driver.find_element_by_id('psdData.serviceType'))
        shipment_type.select_by_value('FedEx Ground')

        # package dims and weight
        shipment_type = Select(driver.find_element_by_id('psd.mps.row.dimensions.0'))

        # TODO: how to wait on Select
        sleep(0.25)

        shipment_type.select_by_value('manual')

        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="psd.mps.row.dimensionLength.0"]'))).send_keys(length)
        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="psd.mps.row.dimensionWidth.0"]'))).send_keys(width)
        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="psd.mps.row.dimensionHeight.0"]'))).send_keys(height)

        input_field_by_xpath('//*[@id="psd.mps.row.weight.0"]', weight)

        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="completeShip.ship.field"]'))).click()

        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm.ship.field"]'))).click()

        image = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="labelImage"]')))

        path = '/mnt/c/Users/Anthony/OneDrive/Desktop/fedex_pdfs/'

        filename = parser.name + datetime.datetime.now().strftime('%f') + '.png'

        with open(path + filename, 'wb') as f:
            driver.execute_script("window.scrollTo(0, 100)") 
            sleep(1)
            f.write(driver.find_element_by_xpath('//*[@id="labelImage"]').screenshot_as_png)

        print('label complete')
        input('kill?')
        exit()


if __name__ == "__main__":
    main()
