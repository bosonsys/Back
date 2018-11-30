import logging
from kiteconnect import KiteTicker
import pymysql.cursors
import time
import pandas as pd
import numpy as np
import numpy_ringbuffer

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='market',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker("qw4l9hh030dgujks", "HI47yJjYYp9ebMQlxCUXO4YNoD8OzEgq")
# kws = KiteTicker("your_api_key", "your_access_token")
sList = [7455745, 4159745, 3050241, 4451329, 1492737, 4701441, 2997505, 625153, 5202177, 3660545, 134657, 1076225]
flag = 1
wList = np.array
# execute SQL query using execute() method.
sql = "INSERT INTO `kite_ticker` (`instrument_token`, `last_price`, `last_quantity`, `volume`," \
        "`buy_quantity`, `sell_quantity`, `change`) VALUES (%s, %s, %s, %s, %s, %s, %s);"

# wList = pd.DataFrame();
# print(df)

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    insert_data(ticks)
    t = time.strftime("%S", time.localtime())
    if(int(t)%30 == 0):
        if(flag == 1):
            print_ts("tick")
            insert_candle(ticks)
            flag = 0
    else:
        flag = 1



def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe(sList)

    # Set RELIANCE to tick in `full` mode.
    # ws.set_mode(ws.MODE_FULL, [738561])


def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()
    connection.close()


def insert_candle(df):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for d in df:
                data = (d['instrument_token'], d['last_price'], d['last_quantity'], d['volume'], d['buy_quantity'], d['sell_quantity'], d['change'])
                cursor.execute(sql, data)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()
    finally:
        print("Done")


def insert_data(df):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for d in df:
                data = (d['instrument_token'], d['last_price'], d['last_quantity'], d['volume'], d['buy_quantity'], d['sell_quantity'], d['change'])
                cursor.execute(sql, data)
                i = wList[d['instrument_token']]
                if (i['high'] < i.lastPrice):
                    i['high']  = i.lastPrice
                if (i['low'] > i.lastPrice):
                    i['low'] = i.lastPrice
                    # cName.push(sd[a])

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        # connection.commit()
    finally:
        print(wList)
        print("Done")


def print_ts(message):
    print("[%s] %s"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message))


# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()

