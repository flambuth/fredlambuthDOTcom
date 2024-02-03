from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, DataRequired, Email, EqualTo, ValidationError
from flask import current_app

class SearchForm(FlaskForm):
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

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    account_creation_password = PasswordField('Account Creation Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_account_creation_password(self, field):
        required_password = current_app.config.get('BLOG_PSWD')
        if field.data != required_password:
            raise ValidationError('Invalid account creation password.')
        
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')
