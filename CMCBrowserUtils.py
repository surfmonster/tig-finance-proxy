from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Config import env, envBool


def getBrowser():
    option = webdriver.ChromeOptions()
    if envBool('headless.enable'):
        option.add_argument('--headless')
    chrome = webdriver.Chrome(options=option, executable_path='/ToolKit/chromedriver.exe')
    chrome.set_page_load_timeout(15)
    return chrome
