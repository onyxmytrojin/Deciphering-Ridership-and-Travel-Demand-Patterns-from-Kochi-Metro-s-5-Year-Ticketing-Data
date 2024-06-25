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

start_month = 7
end_month = 12
start_year = 2017
end_year = 2023

months = get_table_names(start_year,end_year,start_month,end_month)
#find_first_monday()

data_list = []
for month in months:
    data_dict = {}
    cur.execute(f'''SELECT origin,destination,COUNT(*) 
                    FROM {month}
                    WHERE origin != '-1' and destination != '-1' 
                    GROUP BY origin,destination 
                    HAVING origin != destination
                    ''')
    # cur.execute(f''' SELECT DATE(entry_time) AS date_group, COUNT(*)
    #                 FROM trial1
    #                 WHERE origin != '-1' and destination != '-1'
    #                 GROUP BY DATE(entry_time)
    #                 ''')
    dates_count = cur.fetchall()
    
    for i in dates_count:
        data_dict[i[0]+'-'+i[1]]=i[2]
    data_list.append(data_dict)
    
# calculate percentage
# get all keys

keys = []
for i in data_list:
    for j in i.keys():
        if j not in keys:
            keys.append(j)
values = []
for i in data_list:
    values.append([0]*len(keys))
    for j in i.keys():
        index = keys.index(j)
        values[-1][index] = i[j]

# calculate percentage

for i in values:
    sum = 0
    for j in i:
        sum+=j
    for j in range(len(i)):
        if sum==0:
            continue
        i[j] = (i[j]*100)/sum

# print(months)
# print(keys)
# print(values)

transposed_values = list(map(list, zip(*values)))  # Transpose values_lists

fig, ax = plt.subplots(layout="constrained")
for i, values in enumerate(transposed_values):
    # print(keys[i],':',max(values),':',values)
    if max(values)<1:
        continue
    ax.plot(months, values, label=keys[i])
    # print(values)

# plt.ylim(bottom=5)
plt.xticks(rotation=90)
plt.xlabel('Months')
plt.ylabel('Percentage of Passengers carried')
plt.title('Travel Patterns for all routes')
plt.legend()
plt.legend(bbox_to_anchor=(1.00, 1.0), loc='upper left')
# plt.constraine

plt.grid(True)
plt.savefig('myfile.png', bbox_inches="tight")
plt.show()


