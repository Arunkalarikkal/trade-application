import mysql.connector

mydb = mysql.connector.connect(user='myuser', password='mypass', host='localhost', port=3306, database='mt5')
print(mydb)


value_arr = {'gold':0, 'silver':0}

value_arr['gold'] = 1022.25
value_arr['silver'] = 25.88

gold_new = 1000.25
silver_new = 26.88


value_arr['gold_difference'] = gold_new - value_arr['gold']
value_arr['silver_difference'] = silver_new - value_arr['silver']

if value_arr['gold_difference'] < 0:
    value_arr['gold_status'] = 0
else:
    value_arr['gold_status'] = 1


if value_arr['silver_difference'] < 0:
    value_arr['silver_status'] = 0
else:
    value_arr['silver_status'] = 1

gold_percent = 100 * value_arr['gold_difference']
value_arr['gold_percent'] = gold_percent / value_arr['gold']

silver_percent = 100 * value_arr['silver_difference']
value_arr['silver_percent'] = silver_percent / value_arr['silver']




mycursor = mydb.cursor()

sql1 = "UPDATE meta_trade_values SET value = %s, diff = %s, percent = %s, status = %s WHERE name = 'Gold'"
sql2 = "UPDATE meta_trade_values SET value = %s, diff = %s, percent = %s, status = %s WHERE name = 'Silver'"

val1 = (value_arr['gold'], value_arr['gold_difference'], value_arr['gold_percent'], value_arr['gold_status'])
val2 = (value_arr['silver'], value_arr['silver_difference'], value_arr['silver_percent'], value_arr['silver_status'])

mycursor.execute(sql1, val1)
mycursor.execute(sql2, val2)


print(value_arr)
mydb.commit()