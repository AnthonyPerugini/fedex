import sys
import os
import urllib.request
import datetime
from time import sleep
from getpass import getpass
from Parser import AddressParser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.binary_location = r"/usr/bin/google-chrome-stable"

executable_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"

def main():

    # personal creds
    with open('pass.txt') as f:
        username, pswd = f.read().split()

#     assert len(sys.argv) <= 2
#     addr_file = sys.argv[1:]
#     if addr_file:
#         addr_file, = addr_file
#     else:
#         addr_file = None
# 
#     print(addr_file)

    parser = AddressParser()

    opt = input('0 for wheel, 1 for battery, 2 for charger, 3 for manual: ')

    if opt == '3':
        length, width, height, weight = input('length: '), input('width: '), input('height: '), input('weight: ')
    else:
        (length, width, height), weight = {'0': ([28 ,28 ,8], 30), '1': ([8, 8, 16], 8), '2': ([6, 9, 2], 4)}[opt]

    print('confirm parameters below:\n--------')
    parser.dump()
    print('Length, Width, Height: ', length, '" x ', width, '" x ', height, '"', sep='')
    print('Weight: ', weight, 'lbs')
    print('--------')
    if input('[y]/n?: ') == 'n':
        exit()

    with webdriver.Chrome(executable_path=executable_path, options=options) as driver:
        # Login to FedEx, max 5 attempts
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
            input('failed to login, press any key to kill.')
            exit()

        # Open shipping tab
        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/div/nav/div/ul/div[1]/li/a/span'))).click()

        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, 
                            '/html/body/div[1]/header/div/div/nav/div/ul/div[1]/li/div/div[1]/div/a'))).click()

        # input shipping details function
        def input_field_by_xpath(xpath, parser_attr):
            name_field = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, 
                                xpath)))

            count = 0
            while name_field.get_attribute('value') != str(parser_attr).strip() and count < 15:
                x = name_field.get_attribute('value') 
                name_field.send_keys(Keys.CONTROL, 'a')
                name_field.send_keys(Keys.BACK_SPACE)
                name_field.send_keys(parser_attr)
                count += 1

            return name_field


        input_field_by_xpath('//*[@id="toData.contactName"]', parser.name)
        input_field_by_xpath('//*[@id="toData.addressLine1"]', parser.address)
        input_field_by_xpath('//*[@id="toData.zipPostalCode"]', parser.zip)
        input_field_by_xpath('//*[@id="toData.city"]', parser.town)
        sleep(0.5)
        input_field_by_xpath('//*[@id="toData.phoneNumber"]', '9785059671\t')
        sleep(0.5)

        if parser.address2:
            input_field_by_xpath('//*[@id="toData.addressLine2"]', parser.address2)

        state_input = Select(driver.find_element_by_xpath('//*[@id="toData.stateProvinceCode"]'))
        state_input.select_by_value(parser.state)

        shipment_type = Select(driver.find_element_by_id('psdData.serviceType'))
        shipment_type.select_by_value('FedEx Ground')

        # package dims and weight
        shipment_type = Select(driver.find_element_by_id('psd.mps.row.dimensions.0'))
        sleep(0.25)
        shipment_type.select_by_value('manual')

        input_field_by_xpath('//*[@id="psd.mps.row.dimensionLength.0"]', length)
        input_field_by_xpath('//*[@id="psd.mps.row.dimensionWidth.0"]', width)
        input_field_by_xpath('//*[@id="psd.mps.row.dimensionHeight.0"]', height)
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

        input(f'Label sucessfully downloaded to {path}. Press any button to exit.')
        exit(0)


if __name__ == "__main__":
    main()
