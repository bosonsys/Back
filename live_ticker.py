# import numpy as np
# import matplotlib
# matplotlib.use('GTK3Agg')  # or 'GTK3Cairo'
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from sqlalchemy import create_engine

# gs = gridspec.GridSpec(3, 3)
fig1, axes1 = plt.subplots(3, 4)
# fig2, axes2 = plt.subplots(3, 3)

gDate = "2018-11-29 09:00:00"
nDate = "2018-11-29 15:20:00"

engine = create_engine('mysql+pymysql://root:@localhost/market')

def __get_name():
    query = 'SELECT distinct(t.instrument_token), c.tradingsymbol FROM kite_ticker as t, kite_comp as c where c.instrument_token = t.instrument_token and t.inserted_on > "'+gDate+'" and t.inserted_on < "'+nDate+'"';
    df = pd.read_sql_query(query, engine)
    return df

cName = __get_name()

def get_name(t):
    # print(t)
    n = cName.loc[cName['instrument_token'] == t]
    return n.tradingsymbol.any()

def draw_chart(script, i, j, n):
        axes1[i, j].clear()
        axes1[i, j].plot(script['inserted_on'], script['change'])
        # axes1[i, j].plot(script['inserted_on'], script['change'].rolling(21).mean(),label= 'MA 9 days')
        # axes1[i, j].plot(script['inserted_on'], script['change'].rolling(50).mean(),label= 'MA 21 days')
        axes1[i, j].plot(script['inserted_on'], script['change'].rolling(200).mean(),label= 'MA 50 days')
        axes1[i, j].set_title(n)
        axes1[i, j].set_xticklabels([])


def animate(i):
    query = 'SELECT * FROM kite_ticker where inserted_on > "'+gDate+'" and inserted_on < "'+nDate+'"';
    df = pd.read_sql_query(query, engine)

    names = df.instrument_token.unique()
    i = 0
    j = 0
    for name in names:
        hin = df.loc[df['instrument_token'] == name]
        n = get_name(name)
        draw_chart(hin, j, i%4, n)
        if i%4 == 3:
            j +=1
        i +=1


manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
# fig1.subplots_adjust(hspace=0)
ani = animation.FuncAnimation(fig1, animate, interval=500)
plt.show()