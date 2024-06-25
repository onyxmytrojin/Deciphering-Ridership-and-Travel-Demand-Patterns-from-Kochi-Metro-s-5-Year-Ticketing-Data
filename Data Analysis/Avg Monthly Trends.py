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
end_month = 12
start_year = 2017
end_year = 2023

months = get_table_names(start_year,end_year,start_month,end_month)
#find_first_monday()

month_data = []
for month in months:
    cur.execute(f''' SELECT COUNT(*)
                    FROM {month}
                    WHERE origin != '-1' and destination != '-1'
                    ''')
    # cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
    #                 FROM trial1
    #                 WHERE origin != '-1' and destination != '-1'
    #                 GROUP BY DATE(entry_time)
    #                 ''')
    dates_count = cur.fetchall()
    # print(dates_count)
    total = dates_count[0][0]
    cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
                    FROM {month}
                    WHERE origin != '-1' and destination != '-1'
                    GROUP BY DATE(entry_time)
                    ORDER BY DATE(entry_time)
                    ''')
    count = cur.fetchall()
    if len(count)!=0:
        avg = total/len(count)
    else:
        avg=0
    month_data.append(avg)
print(month_data)

x = [i for i in months]
# x = [i.split('_')[0].capitalize() for i in months]
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.plot(x,month_data)
    
plt.xticks(rotation=90)
plt.title(f"Data from {months[0].split('_')[0].capitalize()} {months[0].split('_')[1]} to {months[-1].split('_')[0].capitalize()} {months[-1].split('_')[1]}")
plt.xlabel('Months', fontweight ='bold', fontsize = 15) 
plt.ylabel('Avg daily travel trend', fontweight ='bold', fontsize = 15) 

x=[]
for i in months:
    if 'Aug' in i:
        x.append(i)
    elif 'Jul' in i:
        x.append(i)
    # elif 'Mar' in i:
    #     x.append(i)
    # elif 'Apr' in i:
    #     x.append(i)
    else:
        if len(x) !=0: 
            plt.axvspan(x[0], x[-1], color='yellow', alpha=0.5)
        x=[]
        
 
plt.legend()
plt.show() 