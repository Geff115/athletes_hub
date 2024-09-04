#!/usr/bin/env python3
"""
This file initializes all the Flask extensions that our
application Athletes Hub uses.
"""


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()
