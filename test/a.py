import psycopg2
import db

def check_if_exists(id,k):
    table_name = 'users'
    id_name = 'user_id'
    if k == 1:
        table_name='flight_booking'
        id_name = 'booking_id'
    elif k == 2:
        table_name='hotel_booking'
        id_name = 'booking_id'
    query = "select * from "+table_name+" where "+id_name+" = %s;"
    params = (id,)
    result =db.fetch(query,params)
    if len(result) == 0:
        return False
    else:
        return True

def create_random_id(k):
    import random
    import string
    id  = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    while check_if_exists(id,k):
        id  = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        
    
# create a unique integer user_id from a given username string  
def create_user_id(username):
    import hashlib
    return int(hashlib.sha1(username.encode('utf-8')).hexdigest(), 16) % 10**8

# create a unique integer booking_id from a given time stamp
def create_booking_id(timestamp):
    import time
    import hashlib
    timestamp = str(time.time())
    return int(hashlib.sha1(timestamp.encode('utf-8')).hexdigest(), 16) % 10**8

# generate a unique integer booking_id
def generate_booking_id():
    import time
    import hashlib
    timestamp = str(time.time())
    return int(hashlib.sha1(timestamp.encode('utf-8')).hexdigest(), 16) % 10**8

#generate a unique integer user_id using uuid
def generate_user_id():
    import uuid
    return uuid.uuid4().int & (1<<32)-1

#generate a id by increamenting the last id
def generate_id(k):
    table_name = 'users'
    id_name = 'user_id'
    if k == 1:
        table_name='flight_booking'
        id_name = 'booking_id'
    elif k == 2:
        table_name='hotel_booking'
        id_name = 'booking_id'
    query = "select user_id from "+table_name+" order by "+id_name+" desc limit 1;"
    params = ()
    result = db.fetch(query,params)
    return result[0][0]+1

#get the id from the last_id table and increment it and replace it in the table
def create_id(k):
    id_name = 'user_id'
    if k == 1:
        id_name = 'booking_id'
    elif k == 2:
        id_name = 'booking_id'
    query = "select "+id_name+" from last_id;"
    params = ()
    result = db.fetch(query,params)
    if len(result) == 0:
        query = "insert into last_id(user_id,booking_id) values(%s,%s);"
        params = (1,1)
        db.commit(query,params)
        return 1
    else:
        query = "update last_id set "+id_name+" = "+id_name+" + 1;"
        params = ()
        db.commit(query,params)
        return result[0][1]+1


def connect():
    params = {
    'database': 'group_44',
    'user': 'group_44',
    'password': '0I5nnozTfCaEaw',
    'host': '10.17.50.87',
    'port': 5432
    }
    c = psycopg2.connect(**params)
    return c

# def connect():
#     params = {
#     'database': 'group_22',
#     'user': 'group_22',
#     'password': 'NKyjO7dPvQufB',
#     'host': '10.17.50.232',
#     'port': 5432
#     }
#     c = psycopg2.connect(**params)
#     # c = psycopg2.connect("dbname=group_22")
#     return c

query = '''select rc.flight_ids
    from
        (with recursive reach_carr (f,t,all_ids,flight_ids,last_arr_time,cost) as (
                (select source,dest,ARRAY[source] , ARRAY[fl.flight_id] ,fl.pl_arrival_time, fl.distance
                from flights as fl , airport_codes as ac1 , airport_codes as ac2
                where fl.source = ac1.airportcode and ac1.city = 'Denver'
                and fl.dest = ac2.airportcode limit 10)
                union
                (select rc.f,fl.dest,all_ids || fl.source , flight_ids || fl.flight_id , fl.pl_arrival_time , rc.cost + fl.distance
                from reach_carr as rc,flights as fl , airport_codes as ac1 , airport_codes as ac2
                where (rc.t = fl.source)
                and (rc.f = ac1.airportcode and ac1.city = 'Denver')
                and (rc.t <> ac2.airportcode and ac2.city = 'Albuquerque')
                and fl.dest <> ANY(all_ids)
                and array_length(all_ids,1) < 3 limit 10
                )) select * from reach_carr) as rc , airport_codes as ac1 , airport_codes as ac2
    where (rc.f = ac1.airportcode and ac1.city = 'Denver')
    and (rc.t = ac2.airportcode and ac2.city = 'Albuquerque')
    group by rc.flight_ids , rc.cost;'''

if __name__ == '__main__':
    # print("hello world")
    c = connect()
    cur = c.cursor()
    params = {}
    # cur.execute("""SELECT table_name FROM information_schema.tables
    #    WHERE table_schema = 'public'""")
    # for table in cur.fetchall():
    #     print(table)
    cur.execute(query,params)
    result = cur.fetchall()
    cur.close()
    c.close()
    for res in result:
        print(res)
