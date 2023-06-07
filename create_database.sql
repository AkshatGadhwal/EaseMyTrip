create table users(
    user_id serial,
    username text NOT NULL,
    email text ,
    upassword text,
    is_admin boolean, 
    constraint users_key PRIMARY KEY (user_id),
    constraint unique_username UNIQUE (username)
);

create table airport_codes(
    airport_id INTEGER UNIQUE,
    city text,
    airportcode text,
    constraint airport_key primary key (airport_id)
);

create table flights(
    flight_id serial,
    fl_date DATE,
    op_carrier TEXT,
    source TEXT,
    dest TEXT,
    pl_dep_time INTEGER,
    pl_arrival_time INTEGER,
    distance FLOAT,
    constraint flight_key primary key (flight_id)
   -- CONSTRAINT source_key foreign key (source) REFERENCES airport_codes(airportcode) on delete set null
);

create table flight_booking(
    flight_id serial,
    user_id integer,
    booking_id serial,
    is_cancelled boolean,
    constraint booking_key primary key (booking_id),
    constraint flight_ref foreign key (flight_id) references flights(flight_id) on delete set null,
    constraint user_ref foreign key (user_id) references users(user_id) on delete cascade
);

create table hotels(
    hotel_id integer,
    city text,
    name text,
    address text,
    postalcode text,
    constraint hotel_key primary key (hotel_id)
);

create table hotel_booking(
    hotel_id serial,
    user_id serial,
    start_date  DATE,
    end_date DATE,
    is_cancelled boolean,
    booking_id SERIAL,
    constraint hotelbooking_key primary key (booking_id),
    CONSTRAINT user_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE set null,
    CONSTRAINT hotel_fkey FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE set null
);

create table reviews(
    review_id serial,
    hotel_id integer,
    review_rating real,
    review_text text,
    constraint review_key primary key (review_id),
    constraint hotel_ref foreign key (hotel_id) references hotels(hotel_id) on delete cascade
);

create table cities(
    city text,
    state_name TEXT,
    country_name text,
    latitude FLOAT,
    longitude FLOAT,
    id serial,
    constraint city_key primary key (id)
  --  constraint city_fkey foreign key (city) REFERENCES hotels(city) ON DELETE set NULL,
  --  constraint city_fkey2 foreign key (city) REFERENCES airport_codes(city) ON DELETE set NULL
);

SET datestyle ='ISO ,DMY';
-- \copy airport_codes from 'D:/SEM8/COL362/Project/data/codes.csv' delimiter ',' csv header;
-- \copy flights from 'D:/SEM8/COL362/Project/data/flights.csv' delimiter ',' csv header;
-- \copy hotels from 'D:/SEM8/COL362/Project/data/hotels.csv' delimiter ',' csv header;
-- \copy reviews from 'D:/SEM8/COL362/Project/data/reviews.csv' delimiter ',' csv header;
-- \copy cities from 'D:/SEM8/COL362/Project/data/cities.csv' delimiter ',' csv header;


