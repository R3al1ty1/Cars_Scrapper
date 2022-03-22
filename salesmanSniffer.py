from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# def countCars(salesmanId, parser:webdriver.Firefox):
#     parser.get("")

def getSalesmanNumber(url:str, parser:webdriver.Firefox) -> (str, bool):
    """
    Gathers salesman phone number from required page
    :param url: Url of car page
    :param parser: Selenium parser object
    :return: Tuple of string with phone number and bool with validation of salesman as owner (True if he is)
    """
    parser.get(url)
    button = parser.find_element(by=By.CSS_SELECTOR, value=".css-jj4c2i")
    button.click()
    soup = BeautifulSoup(parser.page_source, 'lxml')
    ownerWindow = soup.find("div", class_="css-a1h7tk e29k6pi1")
    owner = bool(ownerWindow)
    for _ in range(10):
        soup = BeautifulSoup(parser.page_source, 'lxml')
        phoneNumber = soup.find("div", class_="css-1gtpvmj e1i7tubr0")
        if phoneNumber:
            return phoneNumber.text[1:].replace(" ", "-").replace("(", "").replace(")", ""), owner
        time.sleep(0.05)
    return None, owner