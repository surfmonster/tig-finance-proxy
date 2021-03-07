from bs4 import BeautifulSoup
from selenium import webdriver


def getBrowser():
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    chrome = webdriver.Chrome(options=option, executable_path='/ToolKit/chromedriver.exe')
    return chrome
