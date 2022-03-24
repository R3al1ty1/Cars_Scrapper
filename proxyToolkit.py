import psycopg2
import requests
from bs4 import BeautifulSoup
from misc import isHostUp


class Proxynator():
    def __init__(self, proxiesNumber):
        self.activeProxies = []
        self.selectedId = -1
        connection = psycopg2.connect(
            host="194.87.102.109",
            database="CarsDB",
            user="postgres",
            password="CarsScrapper123!",
        )
        cur = connection.cursor()
        #cur.execute("SELECT * FROM misc.proxies WHERE \"Anonymity\"='Hig"'")
        cur.execute("SELECT * FROM misc.proxies WHERE \"Anonymity\"='High'")
        dbProxies = cur.fetchall()
        if proxiesNumber > len(dbProxies):
            proxiesNumber = len(dbProxies)
        for proxy in dbProxies[:proxiesNumber]:
            # if isHostUp(proxy[0]):
            print(proxy[0])
            self.activeProxies.append(f"{proxy[4].lower()}://{proxy[0]}:{proxy[1]}")
        if not self.activeProxies:
            print("NO PROXIES AVALABLE, try again")
    def __next__(self):
        self.selectedId = self.selectedId + 1 if self.selectedId < len(self.activeProxies) - 1 else 0
        return self.activeProxies[self.selectedId]


def getProxies1():
    iterValue = 0
    connection = psycopg2.connect(
        host="194.87.102.109",
        database="CarsDB",
        user="postgres",
        password="CarsScrapper123!",
    )
    cur = connection.cursor()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    while True:
        selectedPage = f"https://hidemy.name/en/proxy-list/?start={iterValue}#list"
        page = requests.get(selectedPage, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.find("tbody")
        tableElements = table.find_all(name="tr")
        if not tableElements:
            break
        for tableElement in tableElements:
            detectedSubelements = tableElement.find_all("td")
            recievedSubelementsData = (detectedSubelements[0].text.strip(),  # IP
                                       detectedSubelements[1].text.strip(),  # PORT
                                       detectedSubelements[2].text.strip(),  # GEO
                                       detectedSubelements[3].text[:-4].strip(),  # PING
                                       detectedSubelements[4].text.strip(),  # CONNECTION TYPE
                                       detectedSubelements[5].text.strip(),  # ANONYMITY
                                       "true")  # IS VALID
            query = "INSERT INTO misc.proxies VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query,
                        recievedSubelementsData)
            connection.commit()
        iterValue += 64
#
# pr = Proxynator(50)
#
# for _ in range(60):
#     print(next(pr))