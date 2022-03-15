import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from transliterate import translit, get_available_language_codes

geckodriverLocation = r"/Users/user/Documents/geckodriver" # Location of geckodriver
firefoxProfile = r"/Users/user/Library/Application Support/Firefox/Profiles/459ixwje.default" # Selected Firefox profile

service = Service(geckodriverLocation) # Setting up location

options = Options()
options.set_preference('profile', firefoxProfile) # Setting up profile
#parser = webdriver.Firefox(service=service, options=options)  # Creating webdriver

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

def brandsGet(parser) -> set:
    parser.get("https://auto.drom.ru")  # Getting web page

    brandsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[5]/div[1]/div[1]/div[3]/form/div/div[1]/div[1]/div/div[1]/input") # Locating list element
    brandsList.send_keys(u" ") # Sending space to show up the list
    gatheredBrands = set() # Creating empty set of car brands

    for _ in range(20):
        soup = BeautifulSoup(parser.page_source, 'lxml') # Creating parser object
        data = soup.find_all('div', class_= 'css-1r0zrug e1uu17r80') # Looking for all elements with car brands name

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
    return(sorted(gatheredBrands))

def modelsGet(brand,parser) -> set:
    brand = brand.lower().replace(" ","_")
    parser.get(f"https://auto.drom.ru/{brand}/")# Getting web page
    try:
        brandsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[5]/div[1]/div[1]/div[2]/form/div/div[1]/div[2]/div/div[1]/input")
    except:
         brandsList = parser.find_element(by=By.XPATH,
                                         value="/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/form/div/div[1]/div[2]/div/div[1]/input")
    modelsList.send_keys(u" ")
    gatheredModels = set()
    for _ in range(20):
        soup = BeautifulSoup(parser.page_source, 'lxml') # Creating parser object
        data = soup.find_all('div', class_= 'css-2qi5nz e154wmfa0') # Looking for all elements with car brands name
        data1 = data[0].find_all('div', class_= 'css-1r0zrug e1uu17r80')
        for element in data1:
            try:
                txt = element.text # Getting raw text from element
                if txt != '' and not "Прочие авто" in txt:
                    txt = translit(txt, "ru", reversed=True) # Transliterating russian brands to english
                    txt = txt[:txt.index("(")].strip() # Removing "(n)" structure from the brand name
                    gatheredModels.add(txt) # Trying to get brand name from selected element, else passing to the next one
            except:
                pass
        scrollElement(modelsList, 8)
    return(sorted(gatheredModels))

def generationGet(brand,model) -> set:
    brand = brand.lower().replace(" ", "_")
    model = model.lower().replace(" ", "_")
    url = f'https://auto.drom.ru/{brand}/{model}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    # parser.get(f"https://auto.drom.ru/{brand}/{model}/")  # Getting web page
    # try:
    #     generationsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/form/div/div[1]/div[3]/div/div/div[1]/button")
    # except:
    #      generationsList = parser.find_element(by=By.XPATH,
    #                                      value="/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/form/div/div[1]/div[3]/div/div/div[1]/button")
    #generationsList.click()
    #gatheredGenerations = set()
    #soup = BeautifulSoup(parser.page_source, 'lxml')  # Creating parser object
    generationsArr = []
    dct = []
    i1 = 1
    while True:
        if requests.get(f'{url}/generation{i1}/').status_code != "404":
            i2 = 1
            dct[i1].append(0)
            while True:
                if requests.get(f'{url}/generation{i1}/restyling{i2}').status_code != "404":
                    dct[i1].append[i2]
                    i2 += 1
                else:
                    break
            i1 += 1
        else:
            break
    return dct
    #data = soup.find_all('div', class_='css-q7s5zv e1i4uopi1')  # Looking for all elements with car brands name
    #data1 = data[0].find_all('div', class_='css-1xktnf etjsiba1')
    #if data == []:
    #    data = soup.find_all('div', class_='css-2qi5nz e154wmfa0')
    #    data1 = data[0].find_all('div', class_='css-1b1okqd e1x0dvi10')
    #for element in data1:
    #    try:
    #        txt = element.text  # Getting raw text from element
    #        if txt != '' and not "Любое поколение" in txt:
    #            txt = translit(txt, "ru", reversed=True)  # Transliterating russian brands to english
    #            txt = txt[:txt.index("(")].strip()  # Removing "(n)" structure from the brand name
    #            gatheredGenerations.add(txt)  # Trying to get brand name from selected element, else passing to the next one
    #    except:
    #        pass
    #return(sorted(gatheredGenerations))
print(generationGet('Toyota','Camry'))