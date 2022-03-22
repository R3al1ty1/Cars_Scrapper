from selenium import webdriver
from selenium.webdriver.common.by import By

def getCarImages(url:str, parser:webdriver.Firefox, getAgain:bool = False) -> [str]:
    """
    Gathers all car images from required page and returns their urls
    :param url: Url of required car
    :param parser: Selenium parser object
    :param getAgain: Boolean, that asks if script should get required page again
    :return: List of urls
    """
    if getAgain:
        parser.get(url)
    outputUrls = []
    nextButton = parser.find_element(by=By.CSS_SELECTOR, value=".css-1irmwwu")
    while True:
        imageUrl = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[1]/a/div/div/div[3]/div/img").get_attribute("srcset").split(",")[1][:-3].strip()
        if imageUrl not in outputUrls:
            outputUrls.append(imageUrl)
        else:
            return outputUrls
        nextButton.click()
