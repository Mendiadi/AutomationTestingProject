import mysql.connector as sq

db = sq.connect(host="localhost",password="Password@12345",user='sa',port=1433)
print(db)


