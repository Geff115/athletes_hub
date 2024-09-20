#!/usr/bin/env python3
"""
Authenticating the routes for users
login/signup or even reset their password
"""


from flask import render_template, redirect
from flask import url_for, flash
from flask import request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from . import auth
from app.models import User
from app.main import main
from app.forms import LoginForm, SignupForm, ResetPasswordForm
from app.extensions import db
import logging


logging.basicConfig(level=logging.DEBUG)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handling login credentials of a user
    """
    form = LoginForm()

    username = None
    password = None

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            # logging.debug(f'Username: {username}, Password: {password}')
        
        # Validating the username and password
        if not username or not password:
            flash("username or password cannot be empty")
            return redirect(url_for('auth.login'))
        elif username and password:
            # Querying the database with the username
            user = User.get_user_by_username(username)
            # Ensuring the user exist in the database
            if user is None:
                flash("The username you have provided does not exist. Please try again.")
                return redirect(url_for('auth.login'))
            
            stored_hash = user.password
            # Safely ensuring that the password is correct for the user
            if check_password_hash(stored_hash, password):
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash("Incorrect password. Please try again or reset your password.")
                return redirect(url_for('auth.login'))
    logging.debug('Rendering login form')
    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Creating a new user and storing the
    user's credentials in the database
    """
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            age = form.age.data
            username = form.username.data
            password = form.password.data
            sport = form.sport.data
            height = form.height.data
            country = form.country.data
            state = form.state.data
            role = form.role.data
            bio = form.bio.data

        # Checking if the user exists in the database
        user = User.get_user_by_username(username)
        if user:
            flash("User already exist, please login into your account")
            return redirect(url_for('auth.login'))
        # Creating the user and storing credentials in the database
        elif user is None:
            hashed_password = generate_password_hash(password)
            user = User(username=username, email=email,
                        password=hashed_password, age=age, first_name=first_name,
                        last_name=last_name, sport=sport, height=height,
                        country=country, state=state, role=role, bio=bio)
            # Adding the user to the database
            db.session.add(user)
            db.session.commit()
            # Success message
            flash("Account created successfully! You will be redirected to login to your account.")
            return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/logout')
def logout():
    """
    Log out the user by using the logout_user function
    in flask_login. It effectively logs out the user by
    removing the user's id from the session
    """
    logout_user()
    flash("Logout successful! Please login again to access your account.")
    return redirect(url_for('main.homepage'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """
    In case of a forgotten password or an incorrect password
    this function handles a password reset for the user
    """
    form = ResetPasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            new_password = form.new_password.data
        user = User.get_user_by_username(username)
        if user:
            hashed_password = generate_password_hash(new_password)
            user.password = hashed_password
            # Updating the password in the database
            db.session.add(user)
            db.session.commit()
            flash("Password reset successful! You can now login with your new password.")
            return redirect(url_for('auth.login'))
        else:
            flash("Incorrect username provided, please check and try again.")
            return redirect(url_for('auth.reset_password'))
    return render_template('reset_password.html', form=form)
