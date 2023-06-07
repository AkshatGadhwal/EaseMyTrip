from wtforms import Form, BooleanField, StringField, PasswordField, validators

class DeleteUserForm(Form):
    username = StringField('Enter the username')