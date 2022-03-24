import time
from datetime import datetime

import psycopg2
#import faster_than_requests as requests
import requests
import threading
from proxyToolkit import Proxynator

def threaded(id:int, conn:psycopg2.connect, proxy:str):
    cur = conn.cursor()
    url = f"https://moscow.drom.ru/volkswagen/touareg/{id}.html"
    proxies = {
        "http":proxy,
        "https":proxy
    }
    try:
        answer = requests.get(url, proxies=proxies, timeout=20)
    except:
        return
    time.sleep(1)
    if answer.status_code == 200:
        cur.execute(f"INSERT INTO main.ads (id,url) VALUES ({id},'{url}')")
        conn.commit()
    elif answer.status_code == 429:
        print("Too many")

connection = psycopg2.connect(
            host = "194.87.102.109",
            database = "CarsDB",
            user = "postgres",
            password = "CarsScrapper123!",
        )

threads = []
start_time = datetime.now()
proxynator = Proxynator(100)
# print(proxynator)
print("Started Threads generation")
for i in range(200):
    t = threading.Thread(target=threaded, args=(10**7 + i, connection, next(proxynator)))
    t.daemon = True
    threads.append(t)
    t.start()
print("Launched")
middle_time = datetime.now()
for thread in threads:
    thread.join()
end_time = datetime.now()
print(middle_time-start_time)
print(end_time-start_time)