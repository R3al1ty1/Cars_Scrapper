import psycopg2

# class connectionDB:
#     def __init__(self):
mydb = psycopg2.connect(
    host = "194.87.102.109",
    database = "CarsDB",
    user = "postgres",
    password = "CarsScrapper123!",
)
#def getCursor(self):
    #    return self.connection.cursor()

temp = mydb.cursor()
sql = "INSERT INTO ads (id,url) VALUES (%s, %s)"
val = ('0', 'Zhora')
temp.execute(sql, val)
temp.commit()