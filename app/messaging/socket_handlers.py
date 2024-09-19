#!/usr/bin/python3

"""
Setting up a NameSpace for messaging to handle
WebSocket events specifically for messaging.
"""


from flask_socketio import Namespace, emit, join_room, leave_room
from flask_socketio import SocketIO
from flask import request
from flask_login import current_user
from app.models import Message, db
from datetime import datetime


socketio = SocketIO()


class MessageNamespace(Namespace):
    """Messaging functionality using Namespace"""

    def on_connect(self):
        # Handling User connection
        print(f"Client connected: {request.sid}")
        emit('connection_success', {'message': 'Successfully connected to the web socket'})

    
    def on_disconnect(self):
        # Handle User disconnection
        print(f"Client disconnected: {request.sid}")

    
    def on_join(self, data):
        # Add a User to a specifc room, (user-to-user conversation)
        room = data['room']
        join_room(room)

        # Fetch previous messages from the database
        previous_messages = Message.query.filter_by(room=room).all()

        # Send previous messages to the client who just joined
        for message in previous_messages:
            emit('new_message', {'user': message.sender_id, 'message': message.content}, to=request.sid)

    
    def on_leave(self, data):
        # Remove a User from a room
        room = data['room']
        leave_room(room)


    def on_send_message(self, data):
        # Handle incoming message from a User
        message_content = data.get('message')
        receiver_id = data.get('receiver_id')

        if message_content and receiver_id:
            sender_id = current_user.id
        
            # Saving the message to the database
            new_message = Message(
                    sender_id=sender_id,
                    receiver_id=receiver_id,
                    content=message_content,
                    timestamp=datetime.utcnow()
            )

            try:
                db.session.add(new_message)
                db.session.commit()

                # Emmitting the message to the receiver (or broadcast to room)
                emit('receive_message', {
                    'message': message_content,
                    'sender': current_user.username,
                    'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'receiver_id': receiver_id
                }, room=receiver_id)
            except Exception as e:
                print(f"Error saving message {e}")
                db.session.rollback()


class NotificationNamespace(Namespace):
    """Notifying users of a new message"""

    def on_connect(self):
        # Handling notifications when the user is connected
        print(f"Client connected for notifications: {request.sid}")
        emit('connection_success', {'message': 'Connected to notifications WebSocket'})


    def on_disconnect(self):
        # Handling notifications when the user is disconnected
        print(f"Client disconnected from notifications: {request.sid}")


    def on_notify(self, data):
        emit('new_notification', data, broadcast=True)

    def on_message_sent(self, data):
        receiver_id = data['receiver_id']
        content = f'You have a new message from {data["sender"]}'

        # Save the notification to the database
        new_notification = Notification(
                user_id=receiver_id,
                message=content,
                timestamp=datetime.utcnow()
        )
        db.session.add(new_notification)
        db.session.commit()

        # Emitting the notification to the receiver
        emit('new_notification', {
            'message': content,
            'timestamp': new_notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True)
