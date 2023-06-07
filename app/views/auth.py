from flask import session

def is_authenticated():
    return session.get('logged_in') and session.get('user_id') != None