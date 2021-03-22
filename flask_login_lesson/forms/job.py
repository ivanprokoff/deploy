from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from sqlalchemy import orm


class JobsForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    team_leader = IntegerField('Team leader id', validators=[DataRequired()])
    work_size = IntegerField('WorkSize', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
