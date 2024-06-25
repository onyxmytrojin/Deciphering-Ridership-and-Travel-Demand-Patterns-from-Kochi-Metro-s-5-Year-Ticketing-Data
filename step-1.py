import psycopg2
import pandas as pd
import os
import datetime
import calendar

def dateToTable(date):
    day,month,year = date.split('/')
def createTables():
    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    temp = cur.fetchall()
    tables = [i[0] for i in temp]
    months = list(calendar.month_name)[1:]
    for i in range(2017,2024):
        for j in months:
            if f"{j}_{i}".lower() not in tables:
                cur.execute(f'''Create Table {j}_{i} (
                                Station VARCHAR(100), 
                                Equipment_Type VARCHAR(10), 
                                Equipment_ID VARCHAR(10), 
                                Fare_Media VARCHAR(10), 
                                Fare_Product VARCHAR(100),
                                Ticket_Number VARCHAR(1000) NOT NULL ,
                                Transaction_Type VARCHAR(20),
                                Fare INT, 
                                Transaction_Time TIMESTAMP NOT NULL);
                                ''')
                conn.commit()
            
    
conn = psycopg2.connect(database = "metromain", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
cur = conn.cursor()
createTables()

directory ="/Users/sarthakgarg/Documents/KMRL Ticket Data"
data_folder = list(os.listdir(directory))
data_folder.remove('.DS_Store')
data_folder.sort()
data_folder.remove('2017')
data_folder.remove('2018')
data_folder.remove('2019')
data_folder.remove('2020')
data_folder.remove('2021')
data_folder.remove('2022')
for folderyear in data_folder:
    year_folder = list(os.listdir(f"/Users/sarthakgarg/Documents/KMRL Ticket Data/{folderyear}"))
    year_folder.remove('.DS_Store')
    year_folder.sort()
    for foldermonth in year_folder:
        month_folder = list(os.listdir(f"/Users/sarthakgarg/Documents/KMRL Ticket Data/{folderyear}/{foldermonth}"))
        month_folder.sort()
        for file in month_folder:
            if file=='.DS_Store':
                continue
            if folderyear=='2023':
                if foldermonth in ['01.Jan 2023','02. Feb 2023','03. March 2023']:
                    continue
                if foldermonth == '04. April 2023':
                    if int(file[:2]) < 25 :
                        continue
            print("Current",file)
            file_loc = f"/Users/sarthakgarg/Documents/KMRL Ticket Data/{folderyear}/{foldermonth}/{file}"
            df = pd.read_excel(file_loc)
            # dataframe1 = dataframe1.
            #	
            i=0
            values = [{} for i in range(7)]
            for row in zip(df['Station'], df['Equipment Type'],df['Equipment ID'], df['Fare Media'],df['Fare Product'],df['Ticket/Card Number'], df['Transaction Type'],df['Fare'],df['Transaction Time']):
                year = row[8].year
                month = row[8].month_name()
                row = list(row)
                row[8]=row[8].round(freq='s')
                if month in values[year%2017].keys():
                    values[year%2017][month].append(tuple(row))
                else:
                    values[year%2017][month]=[tuple(row)]
            months = list(calendar.month_name)[1:]
            for i in range(2017,2024):
                    for j in months:
                        if j in values[i%2017].keys():
                            if values[i%2017][j]:
                                args = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", i).decode('utf-8')
                                                for i in values[i%2017][j])
                                cur.execute(f"INSERT INTO {j}_{i} VALUES " + (args))
                                conn.commit()
conn.commit()
cur.close()
conn.close()