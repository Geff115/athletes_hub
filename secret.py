#!/usr/bin/env python3

"""
Generating a secret key for our
flask application
"""


import secrets
print(secrets.token_urlsafe(50))
