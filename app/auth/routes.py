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
from .__init__ import auth
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handling login credentials of a user
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
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
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password. Please try again or reset your password.")
                return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Creating a new user and storing the
    user's credentials in the database
    """
    if request.method == 'POST':
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        email = request.form.get('email')
        age = request.form.get('age')
        username = request.form.get('username')
        password = request.form.get('password')
        sport = request.form.get('sport')
        height = request.form.get('height')
        country = request.form.get('country')
        state = request.form.get ('state')
        bio = request.form.get('bio')

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
                        country=country, state=state, bio=bio)
            # Adding the user to the database
            db.session.add(user)
            db.session.commit()
            # Success message
            flash("Account created successfully")
            return redirect(url_for('auth.login'))
    return render_template('signup.html')


@auth.route('/logout')
def logout():
    """
    Log out the user by using the logout_user function
    in flask_login. It effectively logs out the user by
    removing the user's id from the session
    """
    logout_user()
    flash("Logout successful! Please login again to access your account.")
    return redirect(url_for('auth.login'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    """
    In case of a forgotten password or an incorrect password
    this function handles a password reset for the user
    """
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new password')
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
    return render_template('reset_password.html')
