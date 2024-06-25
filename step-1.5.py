import psycopg2

conn = psycopg2.connect(database = "metromain", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)
cur = conn.cursor()

cur.execute("select * from information_schema.tables where table_schema='public';")
tables = cur.fetchall()
tables = [i[2] for i in tables]
data = {}
for i in tables:
    cur.execute(f"Select Count(*),fare_product FROM public.{i} Group BY fare_product")
    count = cur.fetchall()
    for j in count:
        if j[1] in data.keys():
            data[j[1]]+=j[0]
        else:
            data[j[1]]=j[0]
    if i=='june_2017':
        pass
print(data)
    