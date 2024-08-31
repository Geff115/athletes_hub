#!/usr/bin/env python3
"""
This file handles the main functionalities for
the authenticated users
"""


from flask import request, render_template, redirect
from flask import url_for, flash
from flask_login import login_required, current_user
from .__init__ import main
from app.models import Athlete, Coach, Message, Notification
from app.forms import ProfileForm


@main.route('/dashboard')
@login_required
def dashboard():
    """
    This is the dashboard route only accessible to users
    who are authenticated.
    It fetches releveant user data, including messages, notifications
    and specific attributes based on the user's role (Athlete or Coach)
    """
    # Fetch user's messages and notifications
    messages = Message.query.filter_by(receiver_id=current_user.id).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).all()

    # Check if the user is an Athlete or Coach, and fetch data accordingly
    user_data = {}
    if current_user.athlete:
        user_data = {
                "role": "Athlete",
                "position": current_user.athlete.position,
                "skills": current_user.athlete.skills,
                "achievements": current_user.athlete.achievements
        }
    elif current_user.coach:
        user_data = {
                "role": "Coach",
                "experience_years": current_user.coach.experience_years,
                "coaching_style": current_user.coach.coaching_style,
                "credentials": current_user.coach.credentials
        }
    # Rendering the dashboard template with the fetched data
    return render_template('dashboard.html', user=current_user,
            messages=messages, notifications=notifications,
            user_data=user_data
    )


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    This route allows users to view and update their profile
    information 
    """
    form = ProfileForm()
    if request.method == 'POST':
        # The user can choose to update their profile information
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.age = form.age.data
            current_user.height = form.height.data
            current_user.country = form.country.data
            current_user.state = form.state.data
            current_user.bio = form.bio.data

            # Update specific fields if user is a Coach or an Athlete
            if current_user.athlete:
                current_user.athlete.position = form.position.data
                current_user.athlete.skills = form.skills.data
                current_user.athlete.achievements = form.achievements.data

            if current_user.coach:
                current_user.coach.experience_years = form.experience_years.data
                current_user.coach.coaching_style = form.coaching_style.data
                current_user.coach.credentials = form.credentials.data

        # saving changes made in the user profile
        db.session.commit()
        flash("Changes in your profile has been update successfully! Taking you back to your dashboard.")
        return redirect(url_for('main.dashboard'))
    # on GET requests, it returns the profile page with the user's current information
    return render_template('profile.html', user=current_user, form=form)
