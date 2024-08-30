"""
The main blueprint will generally handle routes for
the main application pages that are accessible to all
authenticated users.
"""


from flask import Blueprint


main = Blueprint('main', __name__)


from . import routes
