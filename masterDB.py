import psycopg2
from peewee import Model, ModelBase

class connectionDB:
    def __init__(self):
        self.connection = psycopg2.connect(
            host = "194.87.102.109",
            database = "CarsDB",
            user = "postgres",
            password = "CarsScrapper123!",
        )
    def getCursor(self):
        return self.connection.cursor()
    def insert(self,id,url):
        curs = self.getCursor()
        curs.execute(f"INSERT INTO main.ads (id,url) VALUES ({id},'{url}')")
        self.connection.commit()

connection = psycopg2.connect(
            host = "194.87.102.109",
            database = "CarsDB",
            user = "postgres",
            password = "CarsScrapper123!",
        )
# class BaseModel(Model):
#     class Meta:
#         database = connection
#
# class main.ads(ModelBase):
#
# con = connectionDB()
# con.insert(1,"\'Yarik\'")