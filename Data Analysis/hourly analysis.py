import psycopg2
import calendar
import matplotlib.pyplot as plt
import numpy as np
from colour import Color

red = Color("red")
colors = list(red.range_to(Color("green"),31))
for i in range(len(colors)):
    colors[i] = colors[i].rgb

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
end_month = start_month
start_year = 2022
end_year = start_year

months = get_table_names(start_year,end_year,start_month,end_month)
#find_first_monday()

month_data = [[]*24 for i in range(24)]
for month in months:
    week_data = [0]*7
    week_count = [0]*7
    cur.execute(f'''SELECT DATE_TRUNC('hour', entry_time) as hour,DATE(entry_time), count(*) as total_sales 
                    from {month}
                    WHERE origin != '-1' and destination != '-1'
                    GROUP BY Date(entry_time),hour
                    order by hour;
                    ''')
    # cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
    #                 FROM trial1
    #                 WHERE origin != '-1' and destination != '-1'
    #                 GROUP BY DATE(entry_time)
    #                 ''')
    dates_count = cur.fetchall()
    # print(dates_count)
    # date_cur = dates_count[0][0].date()
    # list1 = [0]*24
    for i in dates_count:
        if len(month_data[i[0].hour])==0:
            month_data[i[0].hour] = [0]*31
        # print(month_data,i[0].hour,i[0].day)
        # print('ada',month_data[7])
        month_data[i[0].hour][i[0].day-1]=i[2]
    # for i in dates_count:
    #     day = i[0].weekday()
    #     week_data[day]+=i[1]
    #     week_count[day]+=1
    # avg_weekly = [week_data[i]/week_count[i] for i in range(7)]
    # month_data.append(avg_weekly)
# print(month_data)
# print(len(month_data))

barWidth = 0.05
fig = plt.subplots(figsize =(20, 8))

br = [np.arange(0,31)]
print()
for k in range(1,31):
    print("brprev:",br[k-1])
    brint = [round(x + barWidth,2) for x in br[k-1]]
    print('brint:',brint)
    br.append(brint)
# for i in br:
    # print(br)
    # print('{:.2f}'.format(br))
# print(br)
for k in range(len(month_data)):
    if len(month_data[k])==0:
        continue
    colorfaf = colors[k]
    print(colorfaf)
    print('br:',br[k])
    plt.bar(br[k], month_data[k], width = barWidth, 
        edgecolor = colors ,color = colors)
    if k==10:
        pass


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
# plt.xticks([r + barWidth for r in range(len(month_data[0]))], 
        # range(len(month_data)))
 
plt.legend()
plt.show() 


