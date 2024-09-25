#!/usr/bin/env python3
"""
This file runs the application
"""


from app.__init__ import create_app
from app.messaging.socket_handlers import socketio


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
