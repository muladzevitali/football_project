from wtforms import Form, StringField, validators


class LoginForm(Form):
    username = StringField('username', validators=[validators.required()])
    password = StringField('password', validators=[validators.required()])
