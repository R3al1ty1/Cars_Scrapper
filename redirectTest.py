import requests


r = requests.get('https://shchuchye.drom.ru/nissan/bluebird/45537945.html', allow_redirects=False)
print(r.headers['Location'])