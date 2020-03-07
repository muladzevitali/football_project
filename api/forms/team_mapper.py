from wtforms import Form, StringField, validators

from api.backup.team_links import team_mapper_backup


class TeamsMapper(Form):
    for key, value in team_mapper_backup.items():
        vars()[key] = StringField(f'{key}:', validators=[validators.optional()])
