from flask import Flask, redirect, url_for

#blueprints
from app.views.home_view import home_blueprint
from app.views.profile_view import profile_blueprint
from app.views.login_view import login_blueprint


blueprints = {home_blueprint, profile_blueprint, login_blueprint}

app = Flask(__name__)
app.secret_key = "super secret key"

for bp in blueprints:
    app.register_blueprint(bp)

def unauthorised(e):
    return redirect(url_for('login_blueprint.login'))
app.register_error_handler(401, unauthorised)
