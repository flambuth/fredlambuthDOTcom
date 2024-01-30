from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Length, DataRequired


class CourseForm(FlaskForm):
    '''
    Used in the blog search bar.
    '''
    search_term = StringField('Search: ', validators=[InputRequired(),
                                             Length(min=1, max=100)])





class LoginForm(FlaskForm):
    '''
    For loggin in users to make comments on blog posts.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')