import mysql.connector as sq

db = sq.connect(host="localhost",password="Password@12345",user='CU17')
print(db)
db.disconnect()

