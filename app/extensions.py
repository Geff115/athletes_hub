#!/usr/bin/env python3
"""
This file initializes all the Flask extensions that our
application Athletes Hub uses.
"""


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
