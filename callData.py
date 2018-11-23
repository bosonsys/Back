# import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from sqlalchemy import create_engine

gDate = "2018-11-09 09:00:00"
nDate = "2018-11-09 15:20:00"

engine = create_engine('mysql+pymysql://root:@localhost/market')

def DrawChart(call):
    print(call)
    objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    y_pos = np.arange(len(objects))
    performance = [10, 8, 6, 4, 2, 1]

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, call['nse'])
    plt.ylabel('asef')
    plt.title('Programming language usage')

    plt.show()

def animate():
    callQ = 'SELECT * FROM intra_call where inserted_on > "'+gDate+'" and inserted_on < "'+nDate+'"';
    call = pd.read_sql_query(callQ, engine)
    DrawChart(call)

animate()
# ani = animation.FuncAnimation(plt, animate, interval=5000)
# plt.show()
