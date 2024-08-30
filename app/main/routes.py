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
