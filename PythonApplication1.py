import MetaTrader5 as mt5
import sched, time
from time import sleep
from threading import Timer
import scheduler
import threading 
import time
import mysql.connector

value_arr = {'gold':0, 'silver':0}

mydb = mysql.connector.connect(
  host="localhost",
  user="myuser",
  password="mypass",
  database="mt5"
)

mycursor = mydb.cursor()

 
# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# display data on MetaTrader 5 version


# print(mt5.version())
# connect to the trade account without specifying a password and a server
            # var api = new MT5API(8631960, "dd4444vv", "mt5demo.acetopfx.com", 443);

# now connect to another trading account specifying the password
account=8631960
authorized=mt5.login(account, password="dd4444vv",server="mt5demo.acetopfx.com")
if authorized:
    # display trading account data 'as is'
    # display trading account data in the form of a list
        account_info_dict = mt5.account_info()._asdict()
else:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 

symbol_info=mt5.symbol_info("XAUUSD.DEMO")
if symbol_info!=None:
    symbol_info_dict = mt5.symbol_info("XAUUSD.DEMO")._asdict()
    print(symbol_info_dict['bid'])

# display EURJPY symbol properties

 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
s = sched.scheduler(time.time, time.sleep)
def hello():
    print("Hello %s!")
 
s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
    symbol_info=mt5.symbol_info("XAUUSD.DEMO")
    if symbol_info!=None:
        symbol_info_dict = mt5.symbol_info("XAUUSD.DEMO")._asdict()
        print("XAUUSD.DEMO : ", symbol_info_dict['bid'])
        gold_new = symbol_info_dict['bid']
    
    symbol_info=mt5.symbol_info("XAGUSD.DEMO")
    if symbol_info!=None:
        symbol_info_dict = mt5.symbol_info("XAGUSD.DEMO")._asdict()
        print("XAGUSD.DEMO", symbol_info_dict['bid'])
        silver_new = symbol_info_dict['bid']
    # do your stuff
    s.enter(1, 1, do_something, (sc,))

    value_arr['gold_difference'] = gold_new - value_arr['gold']
    value_arr['silver_difference'] = silver_new - value_arr['silver']
    
    mycursor = mydb.cursor()

    if value_arr['gold_difference'] != 0:
        if value_arr['gold_difference'] < 0:
            value_arr['gold_status'] = 0
        else:
            value_arr['gold_status'] = 1
        
        gold_percent = 100 * value_arr['gold_difference']
        value_arr['gold_percent'] = gold_percent / value_arr['gold']
        value_arr['gold'] = gold_new

        sql = "UPDATE meta_trade_values SET value = %s, diff = %s, percent = %s, status = %s WHERE name = 'Gold'"
        val = (value_arr['gold'], value_arr['gold_difference'], value_arr['gold_percent'], value_arr['gold_status'])
        mycursor.execute(sql, val)


    if value_arr['silver_difference'] != 0:
        if value_arr['silver_difference'] < 0:
            value_arr['silver_status'] = 0
        else:
            value_arr['silver_status'] = 1

        silver_percent = 100 * value_arr['silver_difference']
        value_arr['silver_percent'] = silver_percent / value_arr['silver']
        value_arr['silver'] = silver_new

        sql = "UPDATE meta_trade_values SET value = %s, diff = %s, percent = %s, status = %s WHERE name = 'Silver'"
        val = (value_arr['silver'], value_arr['silver_difference'], value_arr['silver_percent'], value_arr['silver_status'])
        mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

s.enter(1, 1, do_something, (s,))
s.run()
