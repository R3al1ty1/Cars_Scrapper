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
options.headless = True
options.set_preference('profile', firefoxProfile) # Setting up profile
parser = webdriver.Firefox(service=service, options=options)  # Creating webdriver

def getCar(url):
    """
    Требуется переименовать все dataN в нормальные названия, добавить уточнения к переменным с характеристиками машины (like fuelType -> TypeOffuelType)
    Ну и комментарии на английском языке (мне можно на русском, так будет проще)
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    fieldOfSearch = soup.find_all('tr', class_='css-11ylakv ezjvm5n0') #specific row where data is stored (engine, engine volume, mileage etc.)
    foundCarFeatures = {}
    def findName():
        #global soup
        titleName = soup.find_all('h1', class_='css-1tplio9 e18vbajn0')
        carName = titleName[0].find_all('span')[0].text
        carName = carName.split(',')
        carName[0] = carName[0].replace('Продажа', '')
        return(carName[0].strip())
    def findMileage(elem):
        mileage = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        textForamtOfMileage = mileage[0].text
        textForamtOfMileage = textForamtOfMileage.replace('\xa0', '').strip()
        textForamtOfMileage = int(textForamtOfMileage)
        return(textForamtOfMileage)
    def findVolume(elem):
        engineFieldOfSearch = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        engineSpecs = engineFieldOfSearch[0].find_all('span')[0].text
        engineSpecs = engineSpecs.split(',')
        fuelType = engineSpecs[0]
        engineVolume = engineSpecs[1]
        engineVolume = engineVolume.replace('л', '')
        return(fuelType.strip(), engineVolume.strip())
    def findPower(elem):
        powerFieldOfSearch = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        enginePower = powerFieldOfSearch[0].find_all('span')
        textFormatOfPower = enginePower[0].text
        textFormatOfPower = textFormatOfPower.replace('налог', '')
        textFormatOfPower = textFormatOfPower.replace(',', '')
        textFormatOfPower = textFormatOfPower.replace('\xa0', ' ')
        return(textFormatOfPower.strip())
    def findWD(elem):
        carWheelDrive = elem.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
        return(carWheelDrive[0].text.strip())

    foundCarFeatures['Имя'] = findName()
    for gatheredCarFeature in fieldOfSearch:
        requestedCarFeature = gatheredCarFeature.find_all('th', class_='css-1y4xbwk ezjvm5n2')
        textOfRequestedCarFeature = requestedCarFeature[0].text
        if textOfRequestedCarFeature == "Двигатель":
            foundCarFeatures['Топливо'] = findVolume(gatheredCarFeature)[0]
            foundCarFeatures['Объем'] = findVolume(gatheredCarFeature)[1]
        if textOfRequestedCarFeature == "Мощность":
            foundCarFeatures['Мощность'] = findPower(gatheredCarFeature)
        if textOfRequestedCarFeature == "Пробег, км":
            foundCarFeatures['Пробег, км'] = findMileage(gatheredCarFeature)
        if textOfRequestedCarFeature == "Привод":
            foundCarFeatures['Привод'] = findWD(gatheredCarFeature)
    return foundCarFeatures

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
        brandName = soup.find_all('div', class_= 'css-1r0zrug e1uu17r80') # Looking for all elements with car brands name

        for element in brandName:
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

def modelsGet(currentBrand,parser) -> set:
    currentBrand = currentBrand.lower().replace(" ","_")
    parser.get(f"https://auto.drom.ru/{currentBrand}/")# Getting web page
    try:
        brandsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[5]/div[1]/div[1]/div[2]/form/div/div[1]/div[2]/div/div[1]/input")
    except:
         brandsList = parser.find_element(by=By.XPATH,
                                         value="/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/form/div/div[1]/div[2]/div/div[1]/input")
    modelsList.send_keys(u" ")
    gatheredModels = set()
    for _ in range(20):
        soup = BeautifulSoup(parser.page_source, 'lxml') # Creating parser object
        brandNameClass = soup.find_all('div', class_= 'css-2qi5nz e154wmfa0') # Looking for all elements with car brands name
        brandName = brandNameClass[0].find_all('div', class_= 'css-1r0zrug e1uu17r80')
        for element in brandName:
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

def generationGet(currentBrand,model) -> list:
    currentBrand = currentBrand.lower().replace(" ", "_")
    model = model.lower().replace(" ", "_")
    url = f'https://auto.drom.ru/{currentBrand}/{model}/'
    arrOfGenerations = []
    finalArr = []
    newArr = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    parser.get(f"https://auto.drom.ru/{currentBrand}/{model}/")  # Getting web page
    try:
        generationsList = parser.find_element(by=By.XPATH,
                                        value="/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/form/div/div[1]/div[3]/div/div/div[1]/button")
    except:
        generationsList = parser.find_element(by=By.XPATH,
                                        value="/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/form/div/div[1]/div[3]/div/div/div[1]/button")
    generationsList.click()
    gatheredGenerations = list()
    soup = BeautifulSoup(parser.page_source, 'lxml')  # Creating parser object
    isSimplified = True
    brandNameClass = soup.find_all('div', class_='css-2qi5nz e154wmfa0')  # Looking for all elements with car brands name
    if brandNameClass == []:
        brandNameClass = soup.find_all('div', class_='css-q7s5zv e1i4uopi1')
        brandName = brandNameClass[0].find_all('div', class_='css-1xktnf etjsiba1')
        isSimplified = False
    else:
        brandName = brandNameClass[0].find_all('div', class_='css-1b1okqd e1x0dvi10')
    for element in brandName:
        if isSimplified:
            try:
               txt = element.text
               txt = txt.replace('\xa0','')# Getting raw text from element
               if txt != '' and not "Любое поколение" in txt:
                   txt = translit(txt, "ru", reversed=True)  # Transliterating russian brands to english
                   gatheredGenerations.append(txt)  # Trying to get brand name from selected element, else passing to the next one
            except:
               pass
        else:
            data2 = element.find_all('div', class_='css-t5fg4a e162wx9x0')
            data3 = element.find_all('div', class_='css-1bnzx52 e162wx9x0')
            try:
                txt = data2[0].text
                txt = txt.replace('\xa0','')# Getting raw text from element
                if txt != '' and not "Любое поколение" in txt:
                   txt = translit(txt, "ru", reversed=True)  # Transliterating russian brands to english
                   gatheredGenerations.append(txt)  # Trying to get brand name from selected element, else passing to the next one
                txt = data3[0].text  # Getting raw text from element
                if txt != '' and not "Любое поколение" in txt:
                    txt = translit(txt, "ru", reversed=True)  # Transliterating russian brands to english
                    gatheredGenerations.append(txt)  # Trying to get brand name from selected element, else passing to the next one
            except:
                pass
    cnt = 0
    if isSimplified:
        number = 0
        for elem in gatheredGenerations:
            if elem[0] == "-":
                if "restajling" not in elem:
                    restNumber = 0
                    Years = elem[2:].strip()
                else:
                    splitOfGenerationAndYears = elem.split(",")
                    if "-j " not in splitOfGenerationAndYears[0]:
                        restNumber = 1
                        Years = splitOfGenerationAndYears[1].strip()
                    else:
                        restNumber = int(splitOfGenerationAndYears[0][2])
                        Years = splitOfGenerationAndYears[1].strip()
                finalArr.append([Number, restNumber,Frame, Years])
            else:
                Number = int(elem[:elem.index(" ")])
                Frame = elem[elem.index("(") + 1 : elem.index(")")]

    else:
        for elem in gatheredGenerations:
            arrOfGenerations.append(elem)
            cnt += 1
            if cnt == 2:
                newArr.append(arrOfGenerations)
                arrOfGenerations = []
                cnt = 0
        for i in range(len(newArr)):
            splitOfGenerationAndRestyling = newArr[i][1].split(",")
            Number = int(splitOfGenerationAndRestyling[0][0])
            if len(splitOfGenerationAndRestyling) == 1:
                restNumber = 0
            else:
                if "-j " not in splitOfGenerationAndRestyling[1]:
                    restNumber = 1
                else:
                    restNumber = int(splitOfGenerationAndRestyling[1][1])
            splitOfYearsAndFrame = newArr[i][0].split(",",1)
            Frame = splitOfYearsAndFrame[1].strip()
            Years = splitOfYearsAndFrame[0].strip()
            finalArr.append([Number, restNumber, Frame, Years])
    return(finalArr)
#print(generationGet('Toyota','Camry'))
print(getCar('https://moscow.drom.ru/toyota/camry/46333584.html'))
parser.quit()
"""
TODO
P.S. Даю ПОЛНОЕ вето на все нейминги с data. Все старые переименовать в адекватные названия и больше такой ужас не использовать.
И еще: 
1) Проведи форматирование кода через инструменты PyCharm.

"""
