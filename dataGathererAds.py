import time
from datetime import datetime
from tqdm import tqdm

import psycopg2
# import faster_than_requests as requests
import requests as requests
import threading

requests.adapters.DEFAULT_RETRIES = 1
def threaded(id:int, conn:psycopg2.connect, session:requests.session()):
    cur = conn.cursor()
    url = f"https://moscow.drom.ru/volkswagen/touareg/{id}.html"
    answer = session.head(url, timeout=2)
    if answer.status_code == 200:
        cur.execute(f"INSERT INTO main.ads (id,url) VALUES ({id},'{url}')")
        conn.commit()
    elif answer.status_code == 429:
        print(answer.status_code,answer.reason)

#"194.87.102.109"

connection = psycopg2.connect(
            host = "localhost",
            database = "CarsDB",
            user = "postgres",
            password = "CarsScrapper123!",
        )
session = requests.Session()
session.keep_alive = False
threads = []
start_time = datetime.now()
for i in range(50):
    t = threading.Thread(target=threaded, args=(36930000 + i, connection, session))
    t.daemon = True
    threads.append(t)
    t.start()
# for x in range(1000):
#     t = threading.Thread(target=threaded, args=(10**7 + x, connection))
#     t.daemon = True
#     threads.append(t)
#     t.start()
# while len(threads) > 0:
#     threads[0].join()
#     if cnt < mx:
#         t = threading.Thread(target=threaded, args=(10 ** 7 + cnt, connection))
#         t.daemon = True
#         threads.append(t)
#         t.start()
#         threads.pop(0)
#         cnt += 1
#         print(cnt)
ln = len(threads)
for i in tqdm(range(ln)):
    threads[i].join()
end_time = datetime.now()
print(end_time-start_time)