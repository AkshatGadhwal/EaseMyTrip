from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from app.models import get_queries
import json
from app.views.auth import is_authenticated

home_blueprint = Blueprint("home_blueprint", __name__)

@home_blueprint.before_request
def before_request():
    if not is_authenticated():
        flash('You are not Logged in', 'danger')
        return redirect(url_for('login_blueprint.login'))

@home_blueprint.route('/')
@home_blueprint.route('/home')
def home():    
    return render_template('home.html')
    
@home_blueprint.route('/search-city')
def search_cities():
    input = request.args.get('city')
    state = ""
    country = ""
    if request.args.get('state'):
        state = request.args.get('state')
    else:    
        state = ""
    if request.args.get('country'):
        country = request.args.get('country')
    else:
        country = ""
    matches = get_queries.get_cities(city=input,state=state,country=country)
    return jsonify({'data':matches})

@home_blueprint.route('/search-state')
def search_states():
    input = request.args.get('state')
    country = ""
    if request.args.get('country'):
        country = request.args.get('country')
    else:    
        country = ""
    #print(input,country)
    matches = get_queries.get_states(state=input,country=country)
    return jsonify({'data':matches})

@home_blueprint.route('/search-country')
def search_country():
    input = request.args.get('country')
    matches = get_queries.get_countries(country=input)
    return jsonify({'data':matches})

@home_blueprint.route('/search-airport')
def search_airport():
    input = request.args.get('city')
    matches = get_queries.get_airports(city=input)
    return jsonify({'data':matches})

@home_blueprint.route('/flight_booking', methods=['POST'])
def flight_booking():
    city1 = request.form.get('source_city')
    city2 = request.form.get('destination_city')
    fl_date = request.form.get('departure_date')
    flights  = get_queries.get_flights_bw_two_cities(city1,city2,fl_date)
    print(city1,city2,fl_date,flights)
    if flights==[]:
        flights  = get_queries.get_indirect_flights_bw_two_cities(city1,city2,fl_date)
    # return jsonify({'data':flights})
    # flash('Flight Booking Successful', 'success')
    if flights==[]:
        flash('No flights between '+city1+" and "+city2+" on "+fl_date)

    return render_template('home.html', flights=flights)

@home_blueprint.route('/book_flight', methods=['POST'])
def book_flight():
    flight_id = request.form.get('flight_id')
    user_id = session['user_id']
    flight_id = json.loads(flight_id)
    if isinstance(flight_id, list):
        for i in flight_id:
            get_queries.book_flight(i,user_id)
    else:
        get_queries.book_flight(flight_id,user_id)
    flash('Flight Booking Successful', 'success')
    return render_template('home.html')


@home_blueprint.route('/hotel_booking', methods=['POST'])
def hotel_booking():
    city = request.form.get('city')
    hotels = get_queries.get_hotel_order(city)
    if hotels==[]:
        flash('No hotels in '+city)

    return render_template('home.html', hotels= hotels)

@home_blueprint.route('/book_hotel', methods=['POST'])
def book_hotel():
    hotel_id = request.form.get('hotel_id')
    check_in_date = request.form.get('check_in_date')
    check_out_date = request.form.get('check_out_date')
    user_id = session['user_id']
    get_queries.book_hotel(hotel_id,user_id, check_in_date,check_out_date)
    flash('Hotel Booking Successful', 'success')
    return render_template('home.html')



