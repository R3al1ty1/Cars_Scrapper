import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from transliterate import translit, get_available_language_codes


def GetCar(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    crit_arr = ['Двигатель', 'Мощность', 'Пробег, км', 'Привод']
    data = soup.find_all('tr', class_='css-11ylakv ezjvm5n0')
    Features = {}
    def FindName():
        global soup
        data = soup.find_all('h1', class_='css-1tplio9 e18vbajn0')
        data1 = data[0].find_all('span')[0].text
        data1 = data1.split(',')
        data1[0] = data1[0].replace('Продажа', '')
        return(data1[0].strip())
    def FindMileage(elem):
        data = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        return(data[0].text.strip())
    def FindVolume(elem):
        data = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        data1 = data[0].find_all('span')[0].text
        data1 = data1.split(',')
        Fuel = data1[0]
        Volume = data1[1]
        Volume = Volume.replace('л', '')
        return(Fuel.strip(), Volume.strip())
    def FindPower(elem):
        data = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        data1 = data[0].find_all('span')
        temp = data1[0].text
        temp = temp.replace('налог', '')
        temp = temp.replace(',', '')
        return(temp.strip())
    def FindWD(elem):
        data = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        return(data[0].text.strip())

    def getAllHrefs(soupPage:BeautifulSoup):
        return soupPage.find_all(href=True)


    Features['Имя'] = FindName()
    for elem in data:
        data1 = elem.find_all('th', class_='css-1y4xbwk ezjvm5n2')
        data0 = data1[0].text
        if data0 == "Двигатель":
            Features['Двигатель'] = FindVolume(elem)
        if data0 == "Мощность":
            res = FindVolume(elem)
            Fuel = res[0]
            Volume = res[1]
            Features['Топливо'] = Fuel
            Features['Объем'] = Volume
        if data0 == "Пробег, км":
            Features['Пробег, км'] = FindMileage(elem)
        if data0 == "Привод":
            Features['Привод'] = FindWD(elem)
    return Features

def scrollElement(selectedElement, times:int):
    for _ in range(times):
        selectedElement.send_keys(Keys.DOWN) # Emulating press of DOWN button for {times} times

def brandsGet() -> set:

    geckodriverLocation = r"/Users/nasa/Documents/geckodriver" # Location of geckodriver
    firefoxProfile = r"/Users/nasa/Library/Application Support/Firefox/Profiles/0qtiw2tn.default" # Selected Firefox profile
    brandNameCSSClass = 'css-1r0zrug e1uu17r80' # Css class of element with car brand name

    service = Service(geckodriverLocation) # Setting up location

    options = Options()
    options.set_preference('profile', firefoxProfile) # Setting up profile

    parser = webdriver.Firefox(service=service, options=options) # Creating webdriver
    parser.get("https://auto.drom.ru") # Getting web page

    brandsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[5]/div[1]/div[1]/div[3]/form/div/div[1]/div[1]/div/div[1]/input") # Locating list element
    brandsList.send_keys(u" ") # Sending space to show up the list
    gatheredBrands = set() # Creating empty set of car brands

    for _ in range(50):
        soup = BeautifulSoup(parser.page_source, 'lxml') # Creating parser object
        data = soup.find_all('div', class_= brandNameCSSClass) # Looking for all elements with car brands name

        for element in data:
            try:
                txt = element.text # Getting raw text from element
                if txt != '' and not "Прочие авто" in txt and not "Любая модель" in txt:
                    txt = translit(txt, "ru", reversed=True) # Transliterating russian brands to english
                    txt = txt[:txt.index("(")].strip() # Removing "(n)" structure from the brand name
                    gatheredBrands.add(txt) # Trying to get brand name from selected element, else passing to the next one
            except:
                pass
        scrollElement(brandsList, 8) # Scrolling list eight times (emulation of pressing DOWN button eight times)

    print(sorted(gatheredBrands))
    parser.quit()

brandsGet()