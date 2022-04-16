import time
from datetime import datetime

import psycopg2
# import faster_than_requests as requests
import requests
import threading
import fake_headers
from main import addSingleCarToDB, connectionInit
from proxyToolkit import Proxynator


def threaded(id: int, conn: psycopg2.connect, proxy: str):
    cur = conn.cursor()
    url = f"https://moscow.drom.ru/volkswagen/touareg/{id}.html"
    # proxies = {
    #     "http":proxy,
    #     "https":proxy
    # }
    header = fake_headers.Headers().generate()
    try:
        answer = requests.get(url, timeout=3, headers=header)
    except:
        return
    time.sleep(1)
    if answer.status_code == 200:
        cur.execute(f"INSERT INTO main.ads (id,url) VALUES ({id},'{url}')")
        conn.commit()
    elif answer.status_code == 429:
        print(header)
        print("Too many")


def launchThreadsWithProxy(start, count, con, proxy=None):
    global threads
    global maxThreads
    for car in range(start, start + count):
        while len(threads) - 3 >= maxThreads:
            pass
        t = threading.Thread(target=addSingleCarToDB, args=(con, car, False, proxy))
        t.daemon = True
        threads.append(t)
        t.start()
        time.sleep(0.20)
    # for thread in threads:
    #     thread.join()


proxies = [{
    "http": "http://104.226.0.82:80"
}, {
    "http": "http://104.226.0.86:80"
}, {
    "http": "http://50.218.57.69:80"
}, {
    "http": "http://50.217.22.108:80"
}, {
    "http": "http://50.220.21.202:80"
},
]
# "194.87.102.109"
# connection = psycopg2.connect(
#     host="localhost",
#     database="CarsDB",
#     user="postgres",
#     password="CarsScrapper123!",
# )
con = connectionInit()
# threads = []
# start_time = datetime.now()
# proxynator = Proxynator(100)
# print(proxynator)
# addSingleCarToDB(con, 10001775, False, proxy)
# print("Started Threads generation")

start, count = 10 ** 7, 100000
step = count // (len(proxies) + 1)
maxThreads = 2784
mainThreads = []
threads = []
t = threading.Thread(target=launchThreadsWithProxy, args=(start, step, con))
t.daemon = True
threads.append(t)
t.start()
for i in range(1, len(proxies) + 1):
    t = threading.Thread(target=launchThreadsWithProxy, args=(start + step * i, step, con, proxies[i - 1]))
    t.daemon = True
    threads.append(t)
    t.start()
# print("Launched")
# middle_time = datetime.now()
while threads:
    threads.pop(0).join()
for mainThread in mainThreads:
    mainThread.join()
# end_time = datetime.now()
# print(middle_time - start_time)
# print(end_time - start_time)
