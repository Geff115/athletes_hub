#!/usr/bin/env python3
"""
Flask-WTF forms for the routes and templates that
Athletes Hub uses.
"""


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired, Email


class SignupForm(FlaskForm):
    """
    The signup form for the authentication blueprint
    """
    first_name = StringField('First Name', validators=[DataRequired(message='Cannot be empty.')])
    last_name = StringField('Last Name', validators=[DataRequired(message='Cannot be empty.')])
    email = StringField('Email', validators=[DataRequired(message='Cannot be empty.'), Email()])
    age = IntegerField('Age', validators=[DataRequired(message='Cannot be empty.')])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    sport = StringField('Sport', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired(message='Tell the world about you!')])
    submit = SubmitField('Signup')


class ProfileForm(FlaskForm):
    """
    The profile form for users intending to update
    their profile information
    """
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class LoginForm(FlaskForm):
    """
    The login form for users who already have an account,
    either a Coach or an Athlete
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ResetPasswordForm(FlaskForm):
    """
    The reset password form for users who intend
    to reset the password to their account
    """
    username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
