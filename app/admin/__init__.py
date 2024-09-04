"""
Setting up the admin blueprint
"""


from flask import Blueprint


admin = Blueprint('admin', __name__)


from . import routes
