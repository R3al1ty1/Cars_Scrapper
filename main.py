import urllib.request
import requests
from bs4 import BeautifulSoup

cnt = 0
url = 'https://moscow.drom.ru/bmw/3-series/46211372.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)
html = urllib.request.urlopen('https://auto.ru/cars/used/sale/bmw/3er/1106225141-3c6c8b75/')
#response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, 'lxml')
f = open('index.html', 'w')
f.write(html.url)
crit_arr = ['Двигатель', 'Мощность', 'Пробег, км']

def FindName():
    global soup
    data = soup.find_all('h1', class_ = 'CardHead__title')
    return(data[0].text)
def FindData():
    data = soup.find_all('li', class_ = 'CardInfoRow CardInfoRow_year')
    data0 = data[0].find_all('span')
    data1 = data0[1].find_all('a')
    return(data1[0].text)
def FindMileage():
    global soup
    data = soup.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
    return(data[0].text)
def FindVolume():
    global soup
    data = soup.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
    data1 = data[0].find_all('span')
    return(data1[0].text)
def FindPower():
    global soup
    data = soup.find_all('td', class_ = 'css-7whdrf ezjvm5n1')
    data1 = data[0].find_all('span')
    return(data1[0].text)
while cnt != 3:
    data = soup.find_all('th', class_='css-1y4xbwk ezjvm5n2')
    data0 = data[0].text
    if data0 == crit_arr[0]:
        crit_arr.remove(data0)
        if cnt == 0:
            print(FindVolume())
        if cnt == 1:
            print(FindPower())
        if cnt == 2:
            print(FindMileage())
        cnt += 1
    else:
        continue