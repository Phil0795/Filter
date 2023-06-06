import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="Phil",
    passwd="phil",
    database="testdb"
    )

cursor = db.cursor()


