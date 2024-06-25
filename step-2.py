import psycopg2
from datetime import datetime
import copy
import calendar
from tqdm import tqdm

def get_table_names(start_year,end_year,start_month,end_month):
    months = []
    month_names = list(calendar.month_name)
    j=start_month
    for i in range(start_year,end_year+1):
        while not (j>=end_month+1 and i>=end_year):
            if j==13:
                break
            months.append(f"{month_names[j]}_{i}".lower())
            j+=1
        j=1
    return months

def createTables(months):
    cur2.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
    temp = cur2.fetchall()
    tables = [i[0] for i in temp]
    for j in months:
        if j.lower() not in tables:
            cur2.execute(f'''Create table {j} (
                            origin VARCHAR(100),
                            destination VARCHAR(100),
                            fare Integer,
                            type_of_ticket VARCHAR(100),
                            fare_media VARCHAR(10),
                            entry_time TIMESTAMP,
                            exit_time TIMESTAMP,
                            flag_number INTEGER
                            );
                            ''')
            conn2.commit()

conn = psycopg2.connect(database = "metromain", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
conn2 = psycopg2.connect(database = "metro2", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
cur = conn.cursor()
cur2 = conn2.cursor()

start_month = 6
end_month = 12
start_year = 2017
end_year = 2023

months = get_table_names(start_year,end_year,start_month,end_month)
createTables(months)
for table_name in tqdm(months):
    cur.execute(f'''SELECT * FROM {table_name}
                    ORDER BY transaction_time; ''')
    data  = cur.fetchall()
    data_map = {}
    for i in data:
        key = i[5]
        if key in data_map.keys():
            if i[6].lower()=='issue':
                if i[4] in ['SJT']:
                    data_list = [-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key].append(data_list)
                elif i[4] in ['RJT']:
                    data_list = [-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]
                    data_list2 = [-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]
                    data_map[key].append(data_list)
                    data_map[key].append(data_list2)
                elif i[4] in ['Period Pass']:
                    data_list = [-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]
                    data_map[key].append(data_list)
            elif i[6].lower()=='entry':
                if i[4] in ['E-Purse','Trip_Pass']:
                    data_list = [i[0],-1,-1,i[4],i[3],i[8],datetime.now(),-1] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key].append(data_list)
                elif i[4] in ['Period Pass']:
                    if data_map[key][-1][0]==-1:
                        data_map[key][-1][0]= i[0]
                        data_map[key][-1][3] = i[4]
                        data_map[key][-1][5] = i[8]
                    else:
                        data_list = [i[0],-1,-1,i[4],i[3],i[8],datetime.now(),-1]
                        data_map[key].append(data_list)
                elif i[4] in ['SJT','RJT']:
                    for j in range(len(data_map[key])):
                        if data_map[key][j][-1]==-1:
                            data_index=j
                            break
                    data_map[key][j][0] = i[0]
                    data_map[key][j][3] = i[4]
                    data_map[key][j][5] = i[8]
            elif i[6].lower()=='exit':
                if i[4] in ['E-Purse','Trip_Pass']:
                    data_map[key][-1][1] = i[0]
                    data_map[key][-1][2] = i[7]
                    data_map[key][-1][6] = i[8]
                elif i[4] in ['Period Pass']:
                    if data_map[key][-1][1]==-1:
                        data_map[key][-1][1] = i[0]
                        # data_map[key][-1][2] = i[7]
                        data_map[key][-1][6] = i[8]
                    # else:
                    #     data_list = [i[0],-1,-1,i[4],i[3],i[8],datetime.now(),-1]
                    #     data_map[key].append(data_list)
                elif i[4] in ['SJT','RJT']:
                    for j in range(len(data_map[key])):
                        if data_map[key][j][-1]==-1:
                            data_index=j
                            break
                    data_map[key][j][1] = i[0]
                    data_map[key][j][6] = i[8]
            elif i[6].lower()=='cancel':
                del data_map[key]
        else:
            if i[6].lower()=='issue':
                if i[4] in ['SJT']:
                    data_list = [[-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key]=data_list
                elif i[4] in ['RJT']:
                    data_list = [[-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]]
                    data_list2 = [-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]
                    data_map[key]=data_list
                    data_map[key].append(data_list2)
                elif i[4] in ['Period Pass']:
                    data_list = [[-1,-1,i[7],i[4],i[3],datetime.now(),datetime.now(),-1]]
                    data_map[key]=(data_list)
            elif i[6].lower()=='entry':
                if i[4] in ['E-Purse','Trip_Pass']:
                    data_list = [[i[0],-1,-1,i[4],i[3],i[8],datetime.now(),-1]] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key]=data_list
                elif i[4] in ['SJT','RJT']:
                    data_list = [[i[0],-1,i[7],i[4],i[3],i[8],datetime.now(),-1]] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key]=data_list
                elif i[4] in ['Period Pass']:
                    data_list = [[i[0],-1,-1,i[4],i[3],i[8],datetime.now(),-1]]
                    data_map[key]=(data_list)
            elif i[6].lower()=='exit':
                if i[4] in ['E-Purse','Trip_Pass']:
                    data_list = [[-1,i[0],i[7],i[4],i[3],datetime.now(),i[8],-1]] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key]=data_list
                elif i[4] in ['SJT','RJT']:
                    data_list = [[-1,i[0],-1,i[4],i[3],datetime.now(),i[8],-1]] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key]=data_list
                elif i[4] in ['Period Pass']:
                    data_list = [[-1,i[0],-1,i[4],i[3],datetime.now(),i[8],-1]] #[Origin,Destination,Fare,Type of Ticket, Entry Time, Exit Time,Complete_Flag]
                    data_map[key]=data_list
    data=[]
    for i in data_map.keys():
        for j in data_map[i]:
            k = copy.deepcopy(j)
            # k.append(str(i))
            data.append(tuple(k))
    #print(data)
    if len(data)==0:
        continue
    args = ','.join(cur2.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s )", i).decode('utf-8')
                                                    for i in data)
    print(f"START ARGS: {table_name}")
    # print(args)
    # print(f"INSERT INTO {table_name} VALUES " + (args))
    cur2.execute(f"INSERT INTO {table_name} VALUES " + (args))
    conn2.commit()
    print(f"DONE: {table_name}")