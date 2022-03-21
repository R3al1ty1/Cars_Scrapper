import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from transliterate import translit, get_available_language_codes
from string import digits
import time


def countCars(salesmanId, parser:webdriver.Firefox):
    parser.get("")


def getSalesmanNumber(url, parser:webdriver.Firefox):
    parser.get(url)
    button = parser.find_element(by=By.CSS_SELECTOR, value=".css-jj4c2i")
    button.click()
    for _ in range(10):
        soup = BeautifulSoup(parser.page_source, 'lxml')
        phoneNumber = soup.find("div", class_="css-1gtpvmj e1i7tubr0")
        if phoneNumber:
            return phoneNumber.text
        time.sleep(0.05)
    return None