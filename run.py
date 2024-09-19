#!/usr/bin/env python3
"""
This file runs the application
"""


from app.__init__ import create_app
from app.messaging.socket_handlers import socketio


app = create_app()


if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000, debug=True)
