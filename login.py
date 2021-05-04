import sys
import os
from Parser import AddressParser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.binary_location = r"/usr/bin/google-chrome-stable"
executable_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"

def main():

    assert len(sys.argv) <= 2
    addr_file = sys.argv[1:]

    parser = AddressParser(addr_file)
    parser.dump()

    



if __name__ == "__main__":
    main()
