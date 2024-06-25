import psycopg2
import calendar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

def get_table_names(start_year,end_year,start_month,end_month):
    months = []
    month_names = list(calendar.month_name)
    j=start_month
    for i in range(start_year,end_year+1):
        while not (j>=end_month+1 and i>=end_year):
            if j==13:
                break
            months.append(f"{month_names[j]}_{i}")
            j+=1
        j=1
    return months

def find_first_monday():
    day = calendar.weekday(start_year,start_month,1)
    return (8-day)%7


conn = psycopg2.connect(database = "metro2", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
cur = conn.cursor()

start_month = 7
end_month = start_month
start_year = 2023
end_year = start_year
start_date = 1
end_date = 25

months = get_table_names(start_year,end_year,start_month,end_month)
#find_first_monday()
date_data =[]
for month in months:
    cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
                    FROM {month}
                    WHERE origin != '-1' and destination != '-1'
                    GROUP BY DATE(entry_time)
                    ORDER BY DATE(entry_time)
                    ''')
    # cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
    #                 FROM trial1
    #                 WHERE origin != '-1' and destination != '-1'
    #                 GROUP BY DATE(entry_time)
    #                 ''')
    dates_count = cur.fetchall()
    if end_date>=len(dates_count):
        date_data = dates_count[start_date:]
    else:
        date_data = dates_count[start_date:end_date]
    # print(dates_count)


x = [data[0] for data in date_data]
y = [data[1] for data in date_data]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.plot(x,y)
    
plt.xticks(rotation=90)    
plt.xlabel('Months', fontweight ='bold', fontsize = 15) 
plt.ylabel('Avg daily travel', fontweight ='bold', fontsize = 15) 
 
plt.legend()
plt.show() 


