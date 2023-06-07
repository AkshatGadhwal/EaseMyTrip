import app.models.db as db

def generate_id(k):
    table_name = 'users'
    id_name = 'user_id'
    if k == 1:
        table_name='flight_booking'
        id_name = 'booking_id'
    elif k == 2:
        table_name='hotel_booking'
        id_name = 'booking_id'
    query = "select "+id_name +" from "+table_name+" order by "+id_name+" desc limit 1;"
    params = ()
    result = db.fetch(query,params)
    return result[0][0]+1

def get_data_from_id(id, k):
    id_name = "user_id"
    table_name = "users"
    if k == 1:
        id_name = "flight_id"
        table_name = "flights"
    elif k == 2:
        id_name = "hotel_id"
        table_name = "hotels"
    query = "select * from %s where %s = %s"
    params = (table_name, id_name, id)
    data = db.fetch(query, params)
    return data

# User Queries

def get_user(user_id):
    query = "select * from users where user_id = %s;"
    params = (user_id, )
    user = db.fetch(query, params)
    return user

def get_user_by_email(email):
    query = "select * from users where email = %s;"
    params = (email, )
    user = db.fetch(query, params)
    return user

def get_user_by_username(username):
    query = "select * from users where username = %s;"
    params = (username, )
    user = db.fetch(query, params)
    return user

def get_user_by_username_and_upassword(username, upassword):
    query = "select * from users where username = %s and upassword = %s;"
    params = (username, upassword)
    user = db.fetch(query, params)
    return user

def get_user_by_email_and_upassword(email, upassword):
    query = "select * from users where email = %s and upassword = %s;"
    params = (email, upassword)
    user = db.fetch(query, params)
    return user

def get_user_by_username_and_email(username, email):
    query = "select * from users where username = %s and email = %s;"
    params = (username, email)
    user = db.fetch(query, params)
    return user

def get_user_by_username_and_email_and_upassword(username, email, upassword):
    query = "select * from users where username = %s and email = %s and upassword = %s;"
    params = (username, email, upassword)
    user = db.fetch(query, params)
    return user

def register_user(username, email, upassword="password", is_admin = False):
    user_id = generate_id(0)
    query = "insert into users (user_id,username, email, upassword, is_admin) values (%s, %s, %s, %s, %s);"
    params = (user_id, username, email, upassword, is_admin)
    db.commit(query, params)

def update_user_details(username="",email="",upassword="",userid = ""):
    if username!="" :
        query1 = "Update users set username=%s where user_id=%s;"
        params = (username,userid)
        db.commit(query1, params)
        
    if email!="":
        query2 = "Update users set email=%s where user_id=%s;"
        params = (email,userid)
        db.commit(query2, params)
        
    if upassword!="":
        query3 = "Update users set upassword=%s where user_id=%s;"
        params = (upassword,userid)
        db.commit(query3, params)

def delete_user(userid):
    query = "delete from users where user_id=%s;"
    params = (userid,)
    db.commit(query, params)

def delete_user_by_username(username):
    query = "delete from users where username=%s;"
    params = (username,)
    db.commit(query, params)

# Flight Queries

def get_flight(flight_id):
    query = "select * from flights where flight_id = %s;"
    params = (flight_id, )
    flight = db.fetch(query, params)
    return flight

def delete_flight(flight_id):
    query = "delete from flight_booking where flight_id = %s;"
    params = (flight_id, )
    db.commit(query, params)

# def get_user_flights(user_id):
#     query = "select * from flight_booking where user_id = %s;"
#     params = (user_id, )
#     flights = db.fetch(query, params)
#     return flights

def get_flight_bookings(flight_id):
    query = "select * from flight_booking where flight_id = %s;"
    params = (flight_id, )
    flight_booking = db.fetch(query, params)
    return flight_booking

def book_flight(flight_id, user_id):
    booking_id = generate_id(1)
    query = "insert into flight_booking (booking_id, user_id, flight_id, is_cancelled) values (%s, %s, %s, %s);"
    params = (booking_id, user_id, flight_id, False)
    db.commit(query, params)

def book_hotel(hotel_id, user_id, start_date,end_date):
    booking_id = generate_id(2)
    query = "insert into hotel_booking (booking_id, user_id, hotel_id, is_cancelled, start_date, end_date) values (%s, %s, %s, %s,%s,%s);"
    params = (booking_id, user_id, hotel_id, False,start_date,end_date)
    db.commit(query, params)

# Hotel Queries

def get_hotel(hotel_id):
    query = "select * from hotels where hotel_id = %s;"
    params = (hotel_id, )
    hotel = db.fetch(query, params)
    return hotel

def delete_hotel(hotel_id):
    query = "delete from hotel_booking where hotel_id = %s;"
    params = (hotel_id, )
    db.commit(query, params)

def get_hotel_bookings(hotel_id):
    query = "select * from hotel_booking where hotel_id = %s;"
    params = (hotel_id, )
    hotel_booking = db.fetch(query, params)
    return hotel_booking

# def get_user_hotels(user_id):
#     query = "select * from hotel_booking where user_id = %s;"
#     params = (user_id, )
#     hotels = db.fetch(query, params)
#     return hotels

# City Queries

def get_cities(city,state="",country=""):
    query = "select DISTINCT city from cities where LOWER(city) like %s and LOWER(state_name) like %s and LOWER(country_name) like %s limit 20;"
    params = ("{}%".format(city), "{}%".format(state), "{}%".format(country))
    data = db.fetch(query, params)
    print(query)
    print(params)
    print(data)
    return data

def get_states(state, country=""):
    #print("printing state and country")
    print(state, country)
    query = "select DISTINCT state_name, country_name from cities where LOWER(state_name) like %s and LOWER(country_name) like %s limit 20;"
    params = ("{}%".format(state), "{}%".format(country), )
    data = db.fetch(query, params)
    #print("printing data")
    print(query)
    print(params)
    print(data)
    return data

def get_countries(country):
    query = "select DISTINCT country_name from cities where LOWER(country_name) like %s limit 20;"
    params = ("{}%".format(country),)
    data = db.fetch(query, params)
    return data

def get_airports(city = "", state="", country=""):
    query = "select DISTINCT airportcode from airport_codes where LOWER(city) like %s;"
    params = ("{}%".format(city), )
    data = db.fetch(query, params)
    return data

def get_flights_bw_two_cities(city1, city2,fl_date):
    query = "select fl.flight_id, op_carrier , pl_dep_time from airport_codes as city1 JOIN flights as fl ON fl.source = city1.airportcode JOIN airport_codes as city2 ON fl.dest = city2.airportcode WHERE city1.city = %s and city2.city = %s and fl.fl_date = %s;"
    params = (city1, city2, fl_date,)
    data = db.fetch(query, params)
    return data

def get_indirect_flights_bw_two_cities(city1,city2,fl_date):
    query = '''SELECT all_flight_ids, all_flights , planned_times
                FROM 
                (with recursive intermed_cities 
                (from_source,to_dest ,all_flights,planned_times,all_places,all_flight_ids,reach_time,total_distance) as 
                ( (select source ,dest,ARRAY[op_carrier], ARRAY[pl_dep_time],ARRAY[source] , ARRAY[fl.flight_id] ,fl.pl_arrival_time, fl.distance from flights as fl  
                JOIN airport_codes ac1 ON ac1.airportcode = fl.source and ac1.city = %s 
                JOIN airport_codes as ac2 ON ac2.airportcode = fl.dest WHERE fl.fl_date = %s) 
                union (select ic.from_source,fl.dest,all_flights||fl.op_carrier,planned_times||fl.pl_dep_time,all_places || fl.source , ic.all_flight_ids || fl.flight_id , fl.pl_arrival_time , ic.total_distance + fl.distance 
                from intermed_cities as ic JOIN flights as fl ON ic.to_dest = fl.source and fl.pl_dep_time > ic.reach_time 
                JOIN airport_codes as ac1 ON ic.from_source = ac1.airportcode and ac1.city = %s
                JOIN airport_codes as ac2 ON ic.to_dest <> ac2.airportcode and ac2.city = %s
                where fl.dest <> ANY(all_places) and array_length(all_places,1) < 3 and fl_date = %s
                )) select * from intermed_cities) 
                as ic , airport_codes as ac1 , airport_codes as ac2
                where (ic.from_source = ac1.airportcode and ac1.city = %s)
                and (ic.to_dest = ac2.airportcode and ac2.city = %s)
                group by ic.all_places, ic.all_flights,ic.all_flight_ids , planned_times, total_distance
                order by ic.total_distance asc
                limit 10;'''
    params = (city1, fl_date,city1, city2, fl_date,city1,city2)
    data = db.fetch(query, params)
    return data

def get_hotel_order(city):
    query = '''select hotels.hotel_id, name, CAST(AVG(review_rating)as DECIMAL(10,2)) as rating
    from hotels 
    JOIN reviews ON  reviews.hotel_id = hotels.hotel_id
    and hotels.city = %s
    group by hotels.hotel_id 
    order by rating desc;'''
    params = (city,)
    data = db.fetch(query, params)
    print(city)
    print(data)
    return data

def prev_flight_booking(userid):
    query = '''SELECT flights.flight_id,  source, dest,fl_date
    FROM flight_booking 
    JOIN flights on flights.flight_id = flight_booking.flight_id
    JOIN users ON flight_booking.user_id = users.user_id
    WHERE flight_booking.user_id = %s
    ORDER BY fl_date DESC;'''
    params = (userid ,)
    data = db.fetch(query, params)
    return data

def prev_hotel_booking(userid):
    query = '''SELECT hotels.hotel_id,  start_date, end_date, name, city
    FROM hotel_booking 
    JOIN hotels on hotels.hotel_id = hotel_booking.hotel_id
    JOIN users ON hotel_booking.user_id = users.user_id
    WHERE hotel_booking.user_id = %s
    ORDER BY end_date DESC;'''
    params = (userid, )
    data = db.fetch(query, params)
    return data





