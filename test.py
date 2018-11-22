import datetime
# '22-NOV-2018'
d = datetime.datetime.strptime("3-Aug-2018", '%d-%b-%Y').strftime('%Y-%m-%d')
print(d)
