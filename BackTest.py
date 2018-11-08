import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from sqlalchemy import create_engine

gDate = "2018-11-02 09:00:00"
nDate = "2018-11-02 15:20:00"

engine = create_engine('mysql+pymysql://root:@localhost/market')
# query = 'SELECT * FROM marketwatch where updatedTime > \"2018-09-26 \" and updatedTime < \"2018-09-28\"';

query = 'SELECT * FROM kite_watch where insert_on > "'+gDate+'" and insert_on < "'+nDate+'"';
df = pd.read_sql_query(query, engine)
df.set_index('id')
df.head()

callQ = 'SELECT * FROM intra_call where inserted_on > "'+gDate+'"';
call = pd.read_sql_query(callQ, engine)
print(df.head())

# names = df.tradingsymbol.unique()
#print(names)

# With Pands Rolling Function with Percentage
plt.rcParams["figure.figsize"] = (20,8)
fig = plt.figure()
ax1 = plt.subplot2grid((6,1), (0,0), colspan=1, rowspan=5)
ax2 = plt.subplot2grid((6,1), (5,0), colspan=1, sharex=ax1)

def animate(i):
    query = 'SELECT * FROM kite_watch where insert_on > "' + gDate + '" and insert_on < "' + nDate + '"'
    df = pd.read_sql_query(query, engine)
    callQ = 'SELECT * FROM intra_call where inserted_on > "' + gDate + '"'
    call = pd.read_sql_query(callQ, engine)
    # names = df.tradingsymbol.unique()
    names = ['YESBANK']
    for name in names:
        hin = df.loc[df['tradingsymbol'] == name]
        callF = call.loc[call['nse'] == name]
        ax1.clear()
        ax1.plot(hin['insert_on'], hin['change'])
        ax1.plot(hin['insert_on'], hin['change'].rolling(9).mean(),label= 'MA 9 days')
        ax1.plot(hin['insert_on'], hin['change'].rolling(21).mean(),label= 'MA 21 days')
        ax1.plot(hin['insert_on'], hin['change'].rolling(100).mean(),label= 'MA 50 days')
                if row['status'] !=0:
                    plt.annotate('Sell Exit', (row['updated_on'], row['cPer']), textcoords='data')
        ax2.clear()
        ax2.plot(hin['insert_on'], hin['rsi'])
fig.subplots_adjust(hspace=0)
ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()