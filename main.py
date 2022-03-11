import urllib.request
import requests
from bs4 import BeautifulSoup

def GetCar():
    url = 'https://moscow.drom.ru/bmw/3-series/46211372.html'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    html = urllib.request.urlopen('https://auto.ru/cars/used/sale/bmw/3er/1106225141-3c6c8b75/')
    #response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'lxml')
    f = open('index.html', 'w')
    f.write(html.url)
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

    arr.append(FindName())
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