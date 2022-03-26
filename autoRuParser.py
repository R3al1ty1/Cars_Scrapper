import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from transliterate import translit, get_available_language_codes
from fake_headers import Headers
from dateutil.parser import parse
import time

geckodriverLocation = r"/Users/Nasa/Documents/geckodriver" # Location of geckodriver
firefoxProfile = r"/Users/Nasa/Library/Application Support/Firefox/Profiles/459ixwje.default" # Selected Firefox profile

service = Service(geckodriverLocation) # Setting up location

options = Options()
options.headless = False
options.set_preference('profile', firefoxProfile) # Setting up profile
parser = webdriver.Firefox(service=service, options=options)  # Creating webdriver

def yandexCaptchaPass(parser):
    try:
        button = parser.find_element(by=By.CLASS_NAME, value="CheckboxCaptcha-Button")
        button.click()
        time.sleep(1)
    except:
        return

def getCar(url):
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # headers = Headers().generate()
    # print(headers)
    # response = requests.get(url, headers=headers)
    # response.encoding = response.apparent_encoding
    # print(response.content)
    parser.get(url)
    yandexCaptchaPass(parser)
    soup = BeautifulSoup(parser.page_source, 'lxml')
    #fieldOfSearch = soup.find_all('tr', class_='css-11ylakv ezjvm5n0') #specific row where data is stored (engine, engine volume, mileage etc.)
    foundCarFeatures = {}
    def findName():
        titleName = soup.find('h1', class_='CardHead__title')
        carName = titleName.text
        # carName = carName.split(',')
        # nameOfCar = carName[0].replace('Продажа', '')
        return carName
    def findDateOfPublishment():
        months = {"января":"january","февраля":"february",
                  "марта":"march", "апреля": "april",
                  "мая": "may","июня":"june",
                  "июля":"july", "августа":"august",
                  "сентября": "september", "октября":"october",
                  "ноября":"november", "декабря":"december"}
        dateClass = soup.find('div', class_ = 'CardHead__infoItem CardHead__creationDate').text
        #publishDate = dateClass[0].find_all('div', class_ = 'css-pxeubi evnwjo70')[0].text
        dateClass = dateClass.split()
        dateClass[1] = months[dateClass[1]]
        dateClass = "".join(dateClass)
        convertedDate = parse(dateClass)
        convertedDate = f"{convertedDate.day}.{convertedDate.month}.{convertedDate.year}"
        return convertedDate
    def findYear():
        yearOfProduction = soup.find('li', class_='CardInfoRow CardInfoRow_year').find("a")
        # carName = titleName[0].find_all('span')[0].text
        # carName = carName.split(',')
        # yearOfProduction = carName[1][0:5]
        # yearOfProduction = int(yearOfProduction)
        return yearOfProduction.text
    def findMileage():
        mileage = soup.find('li', class_ = 'CardInfoRow CardInfoRow_kmAge').find_all("span")[1]
        # textForamtOfMileage = mileage[0].text
        # textForamtOfMileage = textForamtOfMileage.replace('\xa0', '').strip()
        # textForamtOfMileage = int(textForamtOfMileage)
        return mileage.text[:-3].replace(u"\xa0", "")
    def findEngineParams():
        engineParams = soup.find('li', class_ = 'CardInfoRow CardInfoRow_engine').find_all("span")[1].text.split("/")
        engineParams = [i.strip() for i in engineParams]
        engineParams[0] = engineParams[0][:-2]
        engineParams[1] = engineParams[1][:-5]
        outputParams = []
        volume = [i for i in engineParams if "." in i][0]
        engineParams.pop(engineParams.index(volume))
        hp = [i for i in engineParams if i.isdigit()][0]
        engineParams.pop(engineParams.index(hp))
        engineParams = [volume, hp] + engineParams
        return engineParams
    # def findPower(fieldOfSearch):
    #     powerFieldOfSearch = fieldOfSearch.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
    #     enginePower = powerFieldOfSearch[0].find_all('span')
    #     textFormatOfPower = enginePower[0].text
    #     textFormatOfPower = textFormatOfPower.replace('налог', '')
    #     textFormatOfPower = textFormatOfPower.replace(',', '')
    #     textFormatOfPower = textFormatOfPower.replace('\xa0', ' ')
    #     return(int(textFormatOfPower[:-5]))
    def findWD():
        carWheelDrive = soup.find('li', class_ = 'CardInfoRow CardInfoRow_drive').find_all("span")
        return carWheelDrive[1].text.strip()
    def findColor():
        carColor = soup.find('li', class_ = 'CardInfoRow CardInfoRow_color').find("a")
        return carColor.text.strip()
    def computeTax(hp):
        out = 0
        hp = int(hp)
        if hp <= 100:
            out = hp * 12
        elif 100 < hp <= 125:
            out = hp * 25
        elif 125 < hp <= 150:
            out = hp * 35
        elif 150 < hp <= 175:
            out = hp * 45
        elif 175 < hp <= 200:
            out = hp * 50
        elif 200 < hp <= 225:
            out = hp * 65
        elif 225 < hp <= 250:
            out = hp * 75
        else:
            out = hp * 150
        return out
    def steeringWheelSide():
        sideOfSW = soup.find('li', class_ = 'CardInfoRow CardInfoRow_wheel').find_all("span")
        textFormatOfSide = sideOfSW[1].text.lower()
        isLeftSided = False
        if textFormatOfSide == "левый":
            isLeftSided = True
        return isLeftSided
    def reportAnalyzer():
        reportParams = soup.find_all('span', class_ = 'Link VinReportFreeBlockItem__text')
        carPassportChecker = "не" not in reportParams[0].text
        registrationsNumber = reportParams[3].text.split()[0]
        return(registrationsNumber, carPassportChecker)
    # def findEquipment(fieldOfSearch):
    #     arrOfEquipment = []
    #     carEquipmentClass = fieldOfSearch.find_all('a', class_ = 'css-1n9bvfr e1oy5ngb0')
    #     carEquipment = carEquipmentClass[0]
    #     linkForEquipment = carEquipment.get('href')
    #     response = requests.get(linkForEquipment, headers=headers)
    #     response.encoding = response.apparent_encoding
    #     soup = BeautifulSoup(response.text, 'lxml')
    #     fuelConsumptionClass = soup.find_all('div', class_ = 'b-model-specs__icon b-ico b-ico_type_car-sedan')
    #     fuelConsumption = fuelConsumptionClass[0].find_all('div', class_ = 'b-model-specs__text').text
    #     return(fuelConsumptionClass)

    foundCarFeatures['Имя'] = findName()
    foundCarFeatures['Год'] = findYear()
    foundCarFeatures['Дата публикации'] = findDateOfPublishment()

    foundCarFeatures['Совпадение с ПТС'] = reportAnalyzer()[1]
    foundCarFeatures['Кол-во регистраций'] = reportAnalyzer()[0]
    foundCarFeatures['Объем'], hp, foundCarFeatures['Топливо'] = findEngineParams()
    foundCarFeatures['Мощность, л.с.'] = hp
    foundCarFeatures['Налог'] = computeTax(hp)
    foundCarFeatures['Пробег, км'] = findMileage()
    foundCarFeatures['Привод'] = findWD()
    foundCarFeatures['Цвет'] = findColor()
    foundCarFeatures['Левый руль?'] = steeringWheelSide()
    return foundCarFeatures

def brandsGet(parser) -> set:
    """
    Gets all models from car brand page
    :param parser: Selenium parser object
    :return: Set of found brands
    """
    parser.get("https://auto.ru/himki/cars/all/")  # Getting web page
    yandexCaptchaPass(parser)
    brandsList = parser.find_element(by=By.XPATH, value = "//div[2]/div[2]/div[1]/div/div/div/div/div[1]")
    button = brandsList.find_element(by=By.CLASS_NAME, value="Select__button")
    button.click()# Click to show up the list
    time.sleep(2)
    brandsElemets = parser.find_element(by=By.CLASS_NAME, value="Select__menu")
    soup = BeautifulSoup(parser.page_source, 'lxml')
    brands = set(map(lambda x: x.text, soup.find_all("div", class_="Menu__group")[-1].find_all("div","MenuItem MenuItem_size_m")))

    return(sorted(brands))

def modelsGet(currentBrand:str,parser:webdriver.Firefox) -> set:
    """
    Gets all models from car brand page
    :param currentBrand: Name of selected car brand
    :param parser: Selenium parser object
    :return: Set of found models
    """
    currentBrand = currentBrand.lower().replace(" ","_")
    parser.get(f"https://auto.ru/himki/cars/{currentBrand}/all/")  # Getting web page
    yandexCaptchaPass(parser)
    modelsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[2]/div[3]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div/div[2]")
    button = modelsList.find_element(by=By.CLASS_NAME, value="Select__button")
    button.click()  # Click to show up the list
    time.sleep(2)
    brandsElemets = parser.find_element(by=By.CLASS_NAME, value="Select__menu")
    soup = BeautifulSoup(parser.page_source, 'lxml')
    models = set(map(lambda x: x.text,
                     soup.find_all("div", class_="Menu__group")[-1].find_all("div", "MenuItem MenuItem_size_m")))

    return (sorted(models))

def generationGet(currentBrand:str,model:str) -> list:
    """
    Not completed yet
    :param currentBrand: Name of car brand
    :param model: Name of car model
    :return: List of avalable generations
    """
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
            prodYearsModel = element.find_all('div', class_='css-t5fg4a e162wx9x0')
            genAndRestyling = element.find_all('div', class_='css-1bnzx52 e162wx9x0')
            try:
                txt = prodYearsModel[0].text
                txt = txt.replace('\xa0','')# Getting raw text from element
                if txt != '' and not "Любое поколение" in txt:
                   txt = translit(txt, "ru", reversed=True)  # Transliterating russian brands to english
                   gatheredGenerations.append(txt)  # Trying to get brand name from selected element, else passing to the next one
                txt = genAndRestyling[0].text  # Getting raw text from element
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
#print(getCar('https://auto.ru/cars/used/sale/kia/ceed/1115005703-4fb70fb7/'))
#print(modelsGet("BMW",parser))
parser.quit()