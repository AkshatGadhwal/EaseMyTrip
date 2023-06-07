from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from app.models import get_queries
from app.views.auth import is_authenticated
import app.views.forms.profile_update_form as profile_update_form
import app.views.forms.delete_user_form as delete_user_form
import app.views.forms.RegistrationForm as create_user_form
import app.views.forms.update_user_form as update_user_form



profile_blueprint = Blueprint("profile_blueprint", __name__)

@profile_blueprint.before_request
def before_request():
    if not is_authenticated():
        flash('You are not Logged in', 'danger')
        return redirect(url_for('login_blueprint.login'))

@profile_blueprint.route('/profile')
def profile_page():
    user_id = session['user_id']
    return redirect(url_for('profile_blueprint.profile', userid=user_id))

@profile_blueprint.route('/admin')
def admin_page():
    if session['admin']:
        return redirect(url_for('profile_blueprint.profile', userid=session['user_id']))
    else:
        flash('You are not an admin', 'danger')
        return redirect(url_for('profile_blueprint.profile', userid=session['user_id']))

@profile_blueprint.route('/profile/<userid>')
def profile(userid):
    user_data = get_queries.get_user(userid)[0]
    flight_booking = get_queries.prev_flight_booking(userid)
    hotel_booking = get_queries.prev_hotel_booking(userid)
    print(session['admin'])
    if session['admin']:
        create_form = create_user_form.RegistrationForm(request.form)
        delete_form = delete_user_form.DeleteUserForm(request.form)
        update_form = update_user_form.ProfileUpdateForm(request.form)
        return render_template('admin.html', user_data=user_data, hotels = hotel_booking, flights= flight_booking, create_user_form=create_form, delete_user_form=delete_form, update_user_form=update_form)
    return render_template('profile.html', user_data=user_data, hotels = hotel_booking, flights= flight_booking)

@profile_blueprint.route('/update_profile')
def update_profile_page():
    user_id = session['user_id']
    # return "<h1>update profile</h1>"
    return redirect(url_for('profile_blueprint.update_profile', userid=user_id))

@profile_blueprint.route('/update_profile/<userid>' , methods=['GET','POST'])
def update_profile(userid):
    # Retrieve updated user data from form
    form = profile_update_form.ProfileUpdateForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        get_queries.update_user_details(username,email,password,userid)
        flash('Profile Updated', 'success')
        return redirect(url_for('profile_blueprint.profile', userid=userid))
    user_data = get_queries.get_user(userid)[0]
    return render_template('update_profile.html', form=form, user_data=user_data)

@profile_blueprint.route('/update_by_admin' , methods=['POST'])
def update_by_admin():
    form = update_user_form.ProfileUpdateForm(request.form)
    userid = form.user_id.data
    username = form.username.data
    email = form.email.data
    password = form.password.data
    get_queries.update_user_details(username,email,password,userid)
    flash('Profile Updated', 'success')
    return redirect(url_for('profile_blueprint.profile', userid=session['user_id']))

@profile_blueprint.route('/delete_flight' , methods=['GET', 'POST'])
def delete_flight():
    flight_id = request.form.get('flight_id')
    user_id = session['user_id']
    get_queries.delete_flight(flight_id)
    flash('Flight Booking Deleted', 'success')
    return redirect(url_for('profile_blueprint.profile',userid=user_id))

@profile_blueprint.route('/delete_hotel' ,methods=['GET' , 'POST'])
def delete_hotel():
    hotel_id = request.form.get('hotel_id')
    user_id = session['user_id']
    get_queries.delete_hotel(hotel_id)
    flash('Hotel Booking Deleted', 'success')
    return redirect(url_for('profile_blueprint.profile',userid=user_id))

@profile_blueprint.route('/delete_profile')
def delete_profile_page():
    user_id = session['user_id']
    return redirect(url_for('profile_blueprint.delete_profile', userid=user_id))

@profile_blueprint.route('/delete_profile/<userid>')
def delete_profile(userid):
    get_queries.delete_user(userid)
    return redirect('/login')

@profile_blueprint.route('/delete_by_admin', methods=['POST'])
def delete_by_admin():
    form = delete_user_form.DeleteUserForm(request.form)
    username = form.username.data
    user_id = get_queries.get_user_by_username(username)[0][0]
    if(user_id == session['user_id']):
        flash('You cannot delete yourself', 'danger')
        return redirect(url_for('profile_blueprint.profile_page'))

    if not get_queries.get_user_by_username(username):
        flash('Username does not exists')
        return redirect(url_for('profile_blueprint.profile_page'))
    get_queries.delete_user_by_username(username)
    flash('User Deleted', 'success')
    return redirect(url_for('profile_blueprint.profile', userid=session['user_id']))

