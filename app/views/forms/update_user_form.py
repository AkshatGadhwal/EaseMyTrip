from wtforms import Form, BooleanField, StringField, PasswordField, validators

class ProfileUpdateForm(Form):
    user_id = StringField('User ID')
    username = StringField('New Username')
    email = StringField('New Email Address')
    password = PasswordField('New Password', [
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat New Password')