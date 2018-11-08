import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from sqlalchemy import create_engine

gDate = "2018-11-05 09:00:00"
nDate = "2018-11-05 15:20:00"

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
    name = 'PCJEWELLER'
    query = 'SELECT * FROM kite_watch where tradingsymbol ="'+name+'" and insert_on > "' + gDate + '" and insert_on < "' + nDate + '"'
    df = pd.read_sql_query(query, engine)
    indQ = 'SELECT * FROM indicators where tradingsymbol ="'+name+'" and  insert_on > "' + gDate + '" and insert_on < "' + nDate + '"'
    indVal = pd.read_sql_query(indQ, engine)
    callQ = 'SELECT * FROM intra_call where nse ="'+name+'" and inserted_on > "' + gDate + '"'
    call = pd.read_sql_query(callQ, engine)
    # names = df.tradingsymbol.unique()
    callF = call.loc[call['nse'] == name]
    ax1.clear()
    ax1.plot(df['insert_on'], df['lastPrice'])
    ax1.plot(indVal['insert_on'], indVal['sma1'])
    ax1.plot(indVal['insert_on'], indVal['sma2'])
    # ax1.plot(df['insert_on'], df['lastPrice'].rolling(9).mean(), label= 'MA 9 days')
    # ax1.plot(df['insert_on'], df['lastPrice'].rolling(42).mean(),label= 'MA 42 days')
    # ax1.plot(df['insert_on'], df['lastPrice'].rolling(100).mean(),label= 'MA 50 days')
    plt.xticks(rotation=45)
    for index, row in callF.iterrows():
            if row['call'] == 1:
                ax1.annotate('Buy', (row['inserted_on'], (row['price'] -.2)), textcoords='data')
                if row['status'] !=0:
                    ax1.annotate('Buy Exit', (row['updated_on'], row['cPrice']), textcoords='data')
            if row['call'] == 2:
                ax1.annotate('Sell', (row['inserted_on'], (row['price'] - .2)), textcoords='data')
                if row['status'] !=0:
                    plt.annotate('Sell Exit', (row['updated_on'], row['cPrice']), textcoords='data')
    ax2.clear()
    ax2.plot(indVal['insert_on'], indVal['indicator3'])
fig.subplots_adjust(hspace=0)
animate(5000)
# ani = animation.FuncAnimation(fig, animate, interval=5000)
plt.show()