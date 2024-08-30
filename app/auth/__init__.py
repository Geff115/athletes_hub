"""
Defining and initializing the
authentication blueprint
"""

from flask import Blueprint


auth = Blueprint('auth', __name__)


from . import routes
