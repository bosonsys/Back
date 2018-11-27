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
        "`buy_quantity`, `sell_quantity`) " \
        "VALUES (%s, %s, %s, %s, %s, %s);"


def on_ticks(ws, ticks):
    # Callback to receive ticks.
    # logging.debug("Ticks: {}".format(ticks))
    print(type(ticks))
    # ticks['tradable'].remove()
    # print(ticks)
    for d in ticks:
        # d.remove('tradable')
        del d['tradable'], d['mode'], d['ohlc'], d['average_price'], d['change']
        print(d)
        connection.cursor().execute(sql, d)
    # connection.commit()

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

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()