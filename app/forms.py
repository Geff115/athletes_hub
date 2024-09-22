#!/usr/bin/env python3
"""
Flask-WTF forms for the routes and templates that
Athletes Hub uses.
"""


from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms import SelectField, RadioField, BooleanField
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
    role = SelectField('Role', choices=[('Athlete', 'Athlete'), ('Scout', 'Scout')], validators=[DataRequired()])

    # Athlete specific fields
    position = StringField('Position', validators=[DataRequired(message='What position do you play?')])
    skills = StringField('Skills', validators=[DataRequired(message='What skills do you possess?')])
    achievements = StringField('Achievements', validators=[DataRequired(message='Tell the world anything you boast of')])

    # Scout specific fields
    experience_years = StringField('Years of Experience', validators=[DataRequired()])
    credentials = StringField('Scouting Credentials', validators=[DataRequired()])
    
    bio = TextAreaField('Bio', validators=[DataRequired(message='Tell the world about you!')])
    submit = SubmitField('Sign up')

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        # Validate fields based on the user's role
        if self.role.data == 'Athlete':
            if not self.position.data:
                self.position.errors.append('This field is required for athletes.')
                return False
            if not self.skills.data:
                self.skills.errors.append('This field is required for athletes.')
                return False
            if not self.achievements.data:
                self.achievements.errors.append('This field is required for athletes.')
                return False
        elif self.role.data == 'Scout':
            if not self.experience_years.data:
                self.experience_years.errors.append('This field is required for scouts.')
                return False
            if not self.credentials.data:
                self.credentials.errors.append('This field is required for scouts.')
                return False
        return True


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

    # Fields specific to Athletes
    position = StringField('Position')
    skills = TextAreaField('Skills')
    achievements = TextAreaField('Achievements')

    # Fields specific to Scouts
    experience_years = IntegerField('Years of Experience')
    credentials = TextAreaField('Credentials')

    submit = SubmitField('Update Profile')

class LoginForm(FlaskForm):
    """
    The login form for users who already have an account,
    either a Coach or an Athlete
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class ResetPasswordForm(FlaskForm):
    """
    The reset password form for users who intend
    to reset the password to their account
    """
    username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class ManageUsersForm(FlaskForm):
    """
    This form is only accessible to admin users to handle user
    accounts, i.e activating, deactivating, or deletion
    """
    user = SelectField('Users', choices=[])
    action = RadioField('Action', choices=[('activate', 'Activate'), ('deactivate', 'Deactivate'), ('delete', 'Delete')])
    confirm_delete = BooleanField('Confirm Deletion')
    submit = SubmitField('Submit')
