from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import get_queries

login_blueprint = Blueprint("login_blueprint", __name__)


from wtforms import Form, BooleanField, StringField, PasswordField, validators
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


@login_blueprint.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    session['admin'] = False
    return redirect(url_for('home_blueprint.home'))


@login_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        # handle the case where username or email already exists
        if not get_queries.get_user_by_username(username):
            error = 'Username does not exist'
            print("Username does not exist")
            return render_template('login.html', form=form, error=error)
        if not get_queries.get_user_by_username_and_upassword(username, password):
            error = 'Incorrect password'
            print("Incorrect password")
            return render_template('login.html', form=form, error=error)
        
        #update the session
        session['logged_in'] = True
        user_id = get_queries.get_user_by_username(username)[0][0]
        session['user_id'] = user_id
        if username == 'admin':
            session['admin'] = True
        else:
            session['admin'] = False
        # flash('You are now logged in')
        return redirect(url_for('home_blueprint.home'))
    return render_template('login.html', form=form)

@login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # handle the case where username or email already exists
        if get_queries.get_user_by_username(username):
            flash('Username already exists')
            return redirect(url_for('login_blueprint.register'))
        if get_queries.get_user_by_email(email):
            flash('Email already exists')
            return redirect(url_for('login_blueprint.register'))
        
        #update the session
        is_admin = True if username == 'admin' else False
        get_queries.register_user(username, email, password,is_admin)
        
        flash('Thanks for registering')
        return redirect(url_for('login_blueprint.login'))
    return render_template('register.html', form=form)

@login_blueprint.route('/register_by_admin', methods=['POST'])
def register_by_admin():
    form = RegistrationForm(request.form)
    username = form.username.data
    email = form.email.data
    password = form.password.data
    
    # handle the case where username or email already exists
    if get_queries.get_user_by_username(username):
        flash('Username already exists')
        return redirect(url_for('profile_blueprint.profile_page'))
    if get_queries.get_user_by_email(email):
        flash('Email already exists')
        return redirect(url_for('profile_blueprint.profile_page'))
    
    #update the session
    get_queries.register_user(username, email, password,False)
    
    flash('User registered successfully', 'success')
    return redirect(url_for('profile_blueprint.profile_page'))
