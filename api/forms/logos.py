from wtforms import Form, StringField, validators


class LogosForm(Form):
    id = StringField('id', validators=[validators.required()])
    name = StringField('Name ', validators=[validators.required()])
