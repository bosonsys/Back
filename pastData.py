from io import BytesIO
from zipfile import ZipFile, BadZipfile
import requests
import pymysql.cursors
import datetime
from datetime import date
from dateutil.rrule import rrule, DAILY
import pandas as pd

nseURL = 'https://www.nseindia.com/content/historical/EQUITIES/'

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='market',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# execute SQL query using execute() method.
sql = "INSERT INTO `csvdata` (`SYMBOL`, `SERIES`, `OPEN`, `HIGH`, `LOW`, `CLOSE`, `LAST`, `PREVCLOSE`," \
        "`TOTTRDQTY`, `TOTTRDVAL`, `TIMESTAMP`, `TOTALTRADES`, `ISIN`,`OPENP`, `CLOSEP`) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


def get_zip(file_url):
    url = requests.get(file_url)
    try:
        with ZipFile(BytesIO(url.content)) as zipfile:
            # zipfile =
            zip_names = zipfile.namelist()
            if len(zip_names) == 1:
                file_name = zip_names.pop()
                extracted_file = zipfile.open(file_name)
                return extracted_file
    except BadZipfile:
        print("File not found")
        return

def insert_data(df):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            for k, d in df.iterrows():
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
        print("Done - " + dateC)
        # connection.close()

a = date(2018, 11, 28)
b = date(2018, 11, 28)

for dt in rrule(DAILY, dtstart=a, until=b):
    nse = dt.strftime("%Y/%b/").upper()
    nse = nse + 'cm' + dt.strftime("%d%b%Y").upper()
    URL = nseURL+nse+'bhav.csv.zip'
    file = get_zip(URL)
    if file:
        df = pd.read_csv(file)
        insert_data(df)

connection.close()