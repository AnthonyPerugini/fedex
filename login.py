import sys
import os
import pyperclip as pc

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.binary_location = r"/usr/bin/google-chrome-stable"
executable_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"

def main():
    addr_file = sys.argv[1:]
    if addr_file:
        with open('./file.txt', 'r') as f:
            # remove template at top of file
            addr = f.readlines()[7:]
    else:
        # get address from clipboard if no file
        addr = pc.paste().split('\n')

    split_address = [add.strip() for add in addr]

    print(split_address)



if __name__ == "__main__":
    main()
