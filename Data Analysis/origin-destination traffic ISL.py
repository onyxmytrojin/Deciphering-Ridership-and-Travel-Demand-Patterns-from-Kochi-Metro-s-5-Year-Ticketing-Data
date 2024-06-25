import psycopg2
import calendar
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import datetime


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

ISL = [
    datetime.datetime(2022, 10, 7, 6, 2, 32, 5456).date(),
    datetime.datetime(2022, 10, 16, 6, 2, 32, 5456).date(),
    datetime.datetime(2022, 10, 28, 6, 2, 32, 5456).date(),
    datetime.datetime(2022, 11, 13, 6, 2, 32, 5456).date(),
    datetime.datetime(2022, 12, 11, 6, 2, 32, 5456).date(),
    datetime.datetime(2022, 12, 26, 6, 2, 32, 5456).date()
]

start_month = 10
end_month = 12
start_year = 2022
end_year = 2022

months = get_table_names(start_year,end_year,start_month,end_month)
#find_first_monday()

data_list = []
data_dict = {}
days = []
stations = []

data_list_ISL = []
data_dict_ISL = {}
days_ISL = []
stations_ISL = []
for month in months:
    
    cur.execute(f'''SELECT DATE_TRUNC('hour', entry_time) as hour,DATE(entry_time),origin,destination,COUNT(*) 
                    FROM {month}
                    WHERE origin != '-1' and destination != '-1' 
                    GROUP BY DATE(entry_time),hour,(origin,destination)
                    HAVING origin != destination
                    order by DATE(entry_time)
                    ''')
    # cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
    #                 FROM trial1
    #                 WHERE origin != '-1' and destination != '-1'
    #                 GROUP BY DATE(entry_time)
    #                 ''')
    dates_count = cur.fetchall()
    
    for i in dates_count:
        if i[0].date() in ISL:
            if i[0].date() not in days_ISL:
                days_ISL.append(i[0].date())
            if i[2] not in stations_ISL:
                stations_ISL.append(i[2])
            if i[3] not in stations_ISL:
                stations_ISL.append(i[3])
            key = i[2]+'-'+i[3]
            if key in data_dict_ISL.keys():
                data_dict_ISL[key][i[0].hour] += i[4]
            else:
                data_dict_ISL[key] = [0]*24
                
        else:
            if i[0].date() not in days:
                days.append(i[0].date())
            if i[2] not in stations:
                stations.append(i[2])
            if i[3] not in stations:
                stations.append(i[3])
            key = i[2]+'-'+i[3]
            if key in data_dict.keys():
                data_dict[key][i[0].hour] += i[4]
            else:
                data_dict[key] = [0]*24
            
stations.sort()
stations_ISL.sort()

# print(data_dict)
# print(len(days))

for key in data_dict_ISL.keys():
    for j in range(len(data_dict_ISL[key])):
        data_dict_ISL[key][j] = data_dict_ISL[key][j]/len(days_ISL)
        
for key in data_dict.keys():
    for j in range(len(data_dict[key])):
        data_dict[key][j] = data_dict[key][j]/len(days)
src = []
tar = []
val = []

fig, (ax1,ax2) = plt.subplots(2,figsize =(20, 8))

for key in data_dict.keys():
    if max(data_dict[key])<150:
        continue
    ax1.plot(range(24),data_dict[key],label=key)
    # ori,desti = key.split('-')
    
for key in data_dict_ISL.keys():
    if max(data_dict_ISL[key])<75:
        continue
    ax2.plot(range(24),data_dict_ISL[key],label=key)
    
    
    
    
# fig = go.Figure(data=[go.Sankey(
#     node = dict(
#       pad = 15,
#       thickness = 20,
#       line = dict(color = "black", width = 0.5),
#       label = ["A1", "A2", "B1", "B2", "C1", "C2"],
#       color = "blue"
#     ),
#     link = dict(
#       source = src, # indices correspond to labels, eg A1, A2, A1, B1, ...
#       target = tar,
#       value = val
#   ))])

# fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
# fig.show()
        
# calculate percentage
# get all keys

# keys = []
# for i in data_list:
#     for j in i.keys():
#         if j not in keys:
#             keys.append(j)
# values = []
# for i in data_list:
#     values.append([0]*len(keys))
#     for j in i.keys():
#         index = keys.index(j)
#         values[-1][index] = i[j]



# calculate percentage

# for i in values:
#     sum = 0
#     for j in i:
#         sum+=j
#     for j in range(len(i)):
#         if sum==0:
#             continue
#         i[j] = (i[j]*100)/sum

# print(months)
# print(keys)
# print(values)

# transposed_values = list(map(list, zip(*values)))  # Transpose values_lists

# fig, ax = plt.subplots(layout="constrained")
# for i, values in enumerate(transposed_values):
#     # print(keys[i],':',max(values),':',values)
#     if max(values)>2:
#         continue
#     ax.plot(months, values, label=keys[i])
#     # print(values)

# plt.ylim(bottom=5)
ax1.tick_params('x', labelrotation=90)
ax1.set_xlabel('Hour')
ax1.set_ylabel('Avg Hourly passengers')
ax1.set_title('Travel Patterns for all routes')
ax1.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

ax2.tick_params('x', labelrotation=90)
ax2.set_xlabel('Hour')
ax2.set_ylabel('Avg Hourly passengers')
ax2.set_title('Travel Patterns for all routes ISL')
ax2.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

# plt.constraine
# plt.tight_layout()
plt.grid(True)
# plt.savefig('myfile.png', bbox_inches="tight")
plt.show()


