from wtforms import Form, StringField, validators


class CompanyForm(Form):
    company_name = StringField('name', validators=[validators.required()])
    link = StringField('link', validators=[validators.required()])
