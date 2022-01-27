import mysql.connector

mydb = mysql.connector.connect(user='myuser', password='mypass', host='localhost', port=3306, database='mt5')
print(mydb)

mycursor = mydb.cursor()
mycursor.execute("SELECT trade_value FROM metaproductvalues where product='Gold'")
gold_val = mycursor.fetchone()[0]

print(gold_val)
mydb.commit()