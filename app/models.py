#!/usr/bin/env python3
"""
Setting up the database models for
athletes_hub_db using SQLAlchemy ORM
"""


from app.extensions import db
from flask_login import UserMixin
from datetime import datetime
from enum import Enum


class User(UserMixin, db.Model):
    """
    User table for the users. each model in the database
    will inherit from db.Model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True, default="")
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Defining relationships between models
    sent_messages = db.relationship('Message', primaryjoin="User.id == Message.sender_id", back_populates='sender', foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', primaryjoin="User.id == Message.receiver_id", back_populates='receiver', foreign_keys='Message.receiver_id')
    notifications = db.relationship('Notification', back_populates='user', foreign_keys='Notification.user_id')
    athlete = db.relationship('Athlete', back_populates='user', uselist=False, foreign_keys='Athlete.user_id')
    scout = db.relationship('Scout', back_populates='user', uselist=False, foreign_keys='Scout.user_id')

    def __repr__(self):
        """
        String representation of the User
        """
        return f'<User {self.username}>'

    @classmethod
    def get_user_by_username(cls, username):
        """
        Fetch a user from the database based on the username.
        It returns the user object if found, else None.
        """
        return cls.query.filter_by(username=username).first()


class Athlete(db.Model):
    """
    This is the table for the Athletes playing either
    Basketball or football
    """
    __tablename__ = 'athletes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    height = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    position = db.Column(db.String(50), nullable=False)
    achievements = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text, nullable=True, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Defining relationship between the User and Athlete
    user = db.relationship('User', back_populates='athlete')

    # Defining relationship between Athlete and Media
    media = db.relationship('Media', back_populates='athlete', lazy=True)

    def __repr__(self):
        """
        String representation of an Athlete object
        """
        return f'<Athlete {self.user_id}>'


class Scout(db.Model):
    """
    This is for the Scout, either a Basketball scout
    or a Football scout
    """
    __tablename__ = 'scouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    height = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    experience_years = db.Column(db.Integer, nullable=False)
    credentials = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text, nullable=True, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Defining the relationship between Scout and User
    user = db.relationship('User', back_populates='scout')

    # Defining the relationship between Scout and Media
    media = db.relationship('Media', back_populates='scout', lazy=True)

    def __repr__(self):
        """
        String representation of a Scout object
        """
        return f'<Scout {self.user_id}>'


class MessageStatus(Enum):
    UNREAD = 'unread'
    READ = 'read'


class Message(db.Model):
    """
    Message table in the database for the users to interact.
    i.e Coaches and Athletes.
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Adding a status column for read and unread management
    status = db.Column(db.String(10), default=MessageStatus.UNREAD.value, nullable=False)

    # Defining relationship with the User table explicitly
    sender = db.relationship('User', back_populates='sent_messages', foreign_keys=[sender_id])
    receiver = db.relationship('User', back_populates='received_messages', foreign_keys=[receiver_id])

    def __repr__(self):
        """
        String representation of the messages from the
        sender to the receiver
        """
        return f'Message sent from {self.sender_id} to {self.receiver_id}, status: {self.status}'

    # Helper method to mack a message as read
    def mark_as_read(self):
        self.status = MessageStatus.READ.value
        db.session.commit()


class Notification(db.Model):
    """
    Notifications table for the messages
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Adding an is_read field to track whether a notification has been seen
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    # Defining relationship with the User table
    user = db.relationship('User', back_populates='notifications')

    # Helper function to mark the notification as read
    def mark_as_read(self):
        self.is_read = True
        db.session.commit()

    def __repr__(self):
        """
        String rep for notification of messages to
        the users
        """
        return f'Notification {self.message} for User {self.user_id}'


class Media(db.Model):
    """
    Media table for file uploads
    """
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'), nullable=True)
    scout_id = db.Column(db.Integer, db.ForeignKey('scouts.id'), nullable=True)
    media_url = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)  # 'video', 'image', etc.
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to the athlete and scout
    athlete = db.relationship('Athlete', back_populates='media')
    scout = db.relationship('Scout', back_populates='media')

    def __repr__(self):
        return f'<Media {self.media_url} for Athlete {self.athlete_id}>'
