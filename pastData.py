from io import BytesIO
from zipfile import ZipFile
import requests
import pymysql.cursors
import pandas as pd
import datetime
name = 'https://www.nseindia.com/content/historical/EQUITIES/2018/NOV/cm22NOV2018bhav.csv.zip'

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='market',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# execute SQL query using execute() method.
sql = "INSERT INTO `csvdata` (`SYMBOL`, `SERIES`, `OPEN`, `HIGH`, `LOW`, `CLOSE`, `LAST`, `PREVCLOSE`, `TOTTRDQTY`, `TOTTRDVAL`, `TIMESTAMP`, `TOTALTRADES`, `ISIN`,`OPENP`, `CLOSEP`) " \
"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


def get_zip(file_url):
    url = requests.get(file_url)
    zipfile = ZipFile(BytesIO(url.content))
    zip_names = zipfile.namelist()
    if len(zip_names) == 1:
        file_name = zip_names.pop()
        extracted_file = zipfile.open(file_name)
        return extracted_file

def insert_data(df):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for k, d in df.iterrows():
                # print(d)
                # print(type(d))
                # sym = d.SYMBOL
                if d.loc['SERIES'] == 'EQ' or d.loc['SERIES'] == 'BE':
                    cPer = ((d.loc['CLOSE'] - d.loc['OPEN']) / d.loc['OPEN']) * 100
                    oPer = ((d.loc['OPEN'] - d.loc['PREVCLOSE']) / d.loc['PREVCLOSE']) * 100
                    dateC = datetime.datetime.strptime(d.loc['TIMESTAMP'], '%d-%b-%Y').strftime('%Y-%m-%d')
                    data = (d.loc['SYMBOL'],d.loc['SERIES'],d.loc['OPEN'],d.loc['HIGH'],d.loc['LOW'],d.loc['CLOSE'],d.loc['LAST'],d.loc['PREVCLOSE'],d.loc['TOTTRDQTY'],d.loc['TOTTRDVAL'], dateC, d.loc['TOTALTRADES'],d.loc['ISIN'],oPer,cPer)
                    cursor.execute(sql, data)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()

file = get_zip(name)
df = pd.read_csv(file)
insert_data(df)