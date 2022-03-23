import time
from datetime import datetime

import psycopg2
import faster_than_requests as requests
import threading

def threaded(id:int, conn:psycopg2.connect):
    cur = conn.cursor()
    url = f"https://moscow.drom.ru/volkswagen/touareg/{id}.html"
    answer = requests.get(url)
    time.sleep(1)
    if answer.status_code != 404:
        cur.execute(f"INSERT INTO main.ads (id,url) VALUES ({id},'{url}')")
        conn.commit()

connection = psycopg2.connect(
            host = "194.87.102.109",
            database = "CarsDB",
            user = "postgres",
            password = "CarsScrapper123!",
        )

threads = []
start_time = datetime.now()
for i in range(500):
    t = threading.Thread(target=threaded, args=(10**7 + i, connection))
    t.daemon = True
    threads.append(t)
    t.start()
middle_time = datetime.now()
for thread in threads:
    thread.join()
end_time = datetime.now()
print(middle_time-start_time)
print(end_time-start_time)