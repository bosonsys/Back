# import numpy as np
# import matplotlib
# matplotlib.use('GTK3Agg')  # or 'GTK3Cairo'
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from sqlalchemy import create_engine

# gs = gridspec.GridSpec(3, 3)
fig1, axes1 = plt.subplots(3, 4 )
# fig2, axes2 = plt.subplots(3, 3)

gDate = "2018-11-29 09:00:00"
nDate = "2018-11-29 15:20:00"

engine = create_engine('mysql+pymysql://root:@localhost/market')


def draw_chart(script, i, j):
        axes1[i, j].clear()
        axes1[i, j].plot(script['inserted_on'], script['change'])
        # axes1[i, j].plot(script['insert_on'], script['change'].rolling(9).mean(),label= 'MA 9 days')
        # axes1[i, j].plot(script['insert_on'], script['change'].rolling(50).mean(),label= 'MA 21 days')
        # axes1[i, j].plot(script['insert_on'], script['change'].rolling(80).mean(),label= 'MA 50 days')
        axes1[i, j].set_title(script['instrument_token'].any())
        axes1[i, j].set_xticklabels([])


def animate(i):
    query = 'SELECT * FROM kite_ticker where inserted_on > "'+gDate+'" and inserted_on < "'+nDate+'"';
    df = pd.read_sql_query(query, engine)

    names = df.instrument_token.unique()
    i = 0
    j = 0
    for name in names:
        hin = df.loc[df['instrument_token'] == name]
        draw_chart(hin, j, i%4)
        print(name, j, i%4)
        if i%4 == 3:
            j +=1
        i +=1

manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
# fig1.subplots_adjust(hspace=0)
ani = animation.FuncAnimation(fig1, animate, interval=500)
plt.show()