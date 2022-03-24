import threading
import requests
import masterDB


def getPage(id, master:masterDB.connectionDB):
    if requests.get(f"https://moscow.drom.ru/lexus/es250/{id}.html").status_code != 404:
        pass
        #master.insert(id, f"https://moscow.drom.ru/lexus/es250/{id}.html")

master = masterDB.connectionDB()
threads = []
for i in range(200, 10000):
    t = threading.Thread(target=getPage, args=(10**7+i,master))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()