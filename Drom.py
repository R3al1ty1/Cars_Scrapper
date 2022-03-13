import requests
from bs4 import BeautifulSoup

url = "https://auto.drom.ru/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, 'lxml')
crit_arr = ['Двигатель', 'Мощность', 'Пробег, км', 'Привод']
data = soup.find_all('tr', class_='css-11ylakv ezjvm5n0')