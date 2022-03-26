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

geckodriverLocation = r"/Users/user/Documents/geckodriver" # Location of geckodriver
firefoxProfile = r"/Users/user/Library/Application Support/Firefox/Profiles/459ixwje.default" # Selected Firefox profile

service = Service(geckodriverLocation) # Setting up location

options = Options()
options.headless = True
options.set_preference('profile', firefoxProfile) # Setting up profile
parser = webdriver.Firefox(service=service, options=options)  # Creating webdriver

def getCar(url):
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    headers = Headers().generate()
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    #fieldOfSearch = soup.find_all('tr', class_='css-11ylakv ezjvm5n0') #specific row where data is stored (engine, engine volume, mileage etc.)
    foundCarFeatures = {}
    def findName():
        titleName = soup.find('h1', class_='CardHead__title')
        carName = titleName.text
        # carName = carName.split(',')
        # nameOfCar = carName[0].replace('Продажа', '')
        return carName
    def findDateOfPublishment():
        dateClass = soup.find('div', class_ = 'CardHead__infoItem CardHead__creationDate')
        #publishDate = dateClass[0].find_all('div', class_ = 'css-pxeubi evnwjo70')[0].text
        convertedDate = parse(dateClass.text)
        print(convertedDate)
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
        return mileage.text[:-3]
    def findEngineParams():
        engineParams = soup.find('li', class_ = 'CardInfoRow CardInfoRow_engine').find_all("span")[1].split("/")
        engineParams = [i.strip() for i in engineParams]
        engineParams[0] = engineParams[0][:-2]
        engineParams[1] = engineParams[1][:-5]
        engineParams = set(engineParams)
        # engineSpecs = engineFieldOfSearch[0].find_all('span')[0].text
        # engineSpecs = engineSpecs.split(',')
        # fuelType = engineSpecs[0]
        # engineVolume = engineSpecs[1]
        # engineVolume = engineVolume.replace('л', '')
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
        carColor = soup.find_all('li', class_ = 'CardInfoRow CardInfoRow_color').find("a")
        return carColor.text.strip()
    def computeTax(hp):
        out = 0
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
    def reportAnalyzer(fieldOfSearch):
        reportParams = fieldOfSearch.find_all('span', class_ = 'Link VinReportFreeBlockItem__text')[0].text.lower()
        carPassportChecker = False
        if reportParams[5].text[1] == ' ':
            registrationsNumber = int(reportParams[5].text[0])
        else:
            registrationsNumber = int(reportParams[5].text[:2])
        if reportParams[4].text == "Характеристики  совпадают с ПТС":
            carPassportChecker = True
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

    # foundCarFeatures['Совпадение с ПТС'] = reportAnalyzer(soup)[1]
    # foundCarFeatures['Кол-во регистраций'] = reportAnalyzer(soup)[0]
    # for gatheredCarFeature in fieldOfSearch:
    foundCarFeatures['Объем'], hp, foundCarFeatures['Топливо'] = findEngineParams()
    foundCarFeatures['Мощность, л.с.'] = hp
    foundCarFeatures['Налог'] = computeTax(hp)
    foundCarFeatures['Пробег, км'] = findMileage()
    foundCarFeatures['Привод'] = findWD()
    foundCarFeatures['Цвет'] = findColor()
    foundCarFeatures['Левый руль?'] = steeringWheelSide()
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
        modelsList = parser.find_element(by=By.XPATH, value="/html/body/div[2]/div[5]/div[1]/div[1]/div[2]/form/div/div[1]/div[2]/div/div[1]/input")
    except:
        modelsList = parser.find_element(by=By.XPATH,
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
print(getCar('https://auto.ru/cars/used/sale/kia/ceed/1106577920-df03301d/'))
parser.quit()