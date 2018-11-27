import logging
from kiteconnect import KiteTicker
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='market',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


logging.basicConfig(level=logging.DEBUG)

# Initialise
kws = KiteTicker("qw4l9hh030dgujks", "gHQNS5std0datqlIcOdgLutsXlMNWBEI")
# kws = KiteTicker("your_api_key", "your_access_token")

# execute SQL query using execute() method.

sql = "INSERT INTO `kite_ticker` (`instrument_token`, `last_price`, `last_quantity`, `volume`," \
        "`buy_quantity`, `sell_quantity`, `change`) VALUES (%s, %s, %s, %s, %s, %s, %s);"


def on_ticks(ws, ticks):
    # Callback to receive ticks.
    # logging.debug("Ticks: {}".format(ticks))
    # print(type(ticks))
    insert_data(ticks)

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([738561, 5633])

    # Set RELIANCE to tick in `full` mode.
    # ws.set_mode(ws.MODE_FULL, [738561])

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()
    connection.close()

def insert_data(df):
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

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()