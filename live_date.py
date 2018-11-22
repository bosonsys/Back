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

gDate = "2018-11-22 09:00:00"
nDate = "2018-11-22 15:20:00"

engine = create_engine('mysql+pymysql://root:@localhost/market')

def DrawChart(script, call, i, j):
        # axes1.set_yticks([])
        # subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
        axes1[i, j].clear()
        axes1[i, j].plot(script['insert_on'], script['change'])
        # axes1[i, j].plot(script['insert_on'], script['change'].rolling(9).mean(),label= 'MA 9 days')
        # axes1[i, j].plot(script['insert_on'], script['change'].rolling(50).mean(),label= 'MA 21 days')
        # axes1[i, j].plot(script['insert_on'], script['change'].rolling(80).mean(),label= 'MA 50 days')
        axes1[i, j].set_title(script['tradingsymbol'].any())
        axes1[i, j].set_xticklabels([])
        callF = call.loc[call['nse'] == script['tradingsymbol'].any()]
        for index, row in callF.iterrows():
            if row['call'] == 1:
                axes1[i, j].annotate('Buy', (row['inserted_on'], (row['per'] -.2)), textcoords='data')
                if row['status'] !=0:
                    if row['status'] == 1:
                        axes1[i, j].annotate('Buy Exit', (row['updated_on'], row['cPer']), textcoords='data', color='green')
                    if row['status'] == -1:
                        axes1[i, j].annotate('Buy Exit', (row['updated_on'], row['cPer']), textcoords='data', color='red')
            if row['call'] == 2:
                axes1[i, j].annotate('Sell', (row['inserted_on'], (row['per'] - .2)), textcoords='data')
                if row['status'] !=0:
                    if row['status'] == 1:
                        axes1[i, j].annotate('Sell Exit', (row['updated_on'], row['cPer']), textcoords='data', color='green')
                    if row['status'] == -1:
                        axes1[i, j].annotate('Sell Exit', (row['updated_on'], row['cPer']), textcoords='data', color='red')

def animate(i):
    query = 'SELECT * FROM kite_watch where insert_on > "'+gDate+'" and insert_on < "'+nDate+'"';
    df = pd.read_sql_query(query, engine)

    callQ = 'SELECT * FROM intra_call where inserted_on > "'+gDate+'"';
    call = pd.read_sql_query(callQ, engine)

    names = df.tradingsymbol.unique()
    # print(len(names))
    # names = ['IRB','CANFINHOME', 'CUMMINSIND', 'RICOAUTO', 'MOTHERSUMI', 'TECHM', 'TORNTPOWER', 'INFIBEAM', 'PNBHOUSING', 'IBULHSGFIN']
    i = 0
    j = 0
    for name in names:
        hin = df.loc[df['tradingsymbol'] == name]
        DrawChart(hin, call, j, i%4)
        print(name, j, i%4)
        if i%4 == 3:
            j +=1
        i +=1

manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())
# fig1.subplots_adjust(hspace=0)
ani = animation.FuncAnimation(fig1, animate, interval=5000)
plt.show()