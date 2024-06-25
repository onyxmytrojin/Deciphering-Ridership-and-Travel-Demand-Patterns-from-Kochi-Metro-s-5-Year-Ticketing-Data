import psycopg2
import calendar
import matplotlib.pyplot as plt
import numpy as np

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

start_month = 6
end_month = 11
start_year = 2023
end_year = 2023

months = get_table_names(start_year,end_year,start_month,end_month)
#find_first_monday()

month_data =[]
for month in months:
    week_data = [0]*7
    week_count = [0]*7
    cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
                    FROM {month}
                    WHERE origin != '-1' and destination != '-1'
                    GROUP BY DATE(entry_time)
                    ''')
    # cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
    #                 FROM trial1
    #                 WHERE origin != '-1' and destination != '-1'
    #                 GROUP BY DATE(entry_time)
    #                 ''')
    dates_count = cur.fetchall()
    
    for i in dates_count:
        day = i[0].weekday()
        week_data[day]+=i[1]
        week_count[day]+=1
    avg_weekly = [week_data[i]/week_count[i] for i in range(7)]
    month_data.append(avg_weekly)
print(month_data)


barWidth = 0.1
fig = plt.subplots(figsize =(20, 8))

br = [np.arange(len(month_data[0]))]

for k in range(1,len(months)):
    br.append([x + barWidth for x in br[k-1]])
for k in range(len(months)):
    plt.bar(br[k], month_data[k], width = barWidth, 
        edgecolor ='grey', label =months[k][:3])


# br1 = np.arange(len(month_data[0])) 
# br2 = [x + barWidth for x in br1] 
# br3 = [x + barWidth for x in br2] 
 
# # Make the plot
# plt.bar(br1, month_data[0], color ='r', width = barWidth, 
#         edgecolor ='grey', label ='Jun') 
# plt.bar(br2, month_data[1], color ='g', width = barWidth, 
#         edgecolor ='grey', label ='July') 
# plt.bar(br3, month_data[2], color ='b', width = barWidth, 
#         edgecolor ='grey', label ='Aug') 
 
# Adding Xticks 
plt.xlabel('Months', fontweight ='bold', fontsize = 15) 
plt.ylabel('Avg daily travel', fontweight ='bold', fontsize = 15) 
plt.xticks([r + barWidth for r in range(len(month_data[0]))], 
        ['Mon', 'Tue', 'Wed', 'Thur', 'Fri','Sat','Sun'])
 
plt.legend()
plt.show() 


