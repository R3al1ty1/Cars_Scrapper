import requests


r = requests.get('https://novosibirsk.drom.ru/toyota/camry/10000003.html', allow_redirects=False)
# print(r.headers['Location'])
print(r.status_code)