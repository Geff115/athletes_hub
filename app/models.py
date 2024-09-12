#!/usr/bin/env python3
"""
Setting up the database models for
athletes_hub_db using SQLAlchemy ORM
"""


from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """
    User table for the users. each model in the database
    will inherit from db.Model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Defining relationships between models
    sent_messages = db.relationship('Message', primaryjoin="User.id == Message.sender_id", back_populates='sender', foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', primaryjoin="User.id == Message.receiver_id", back_populates='receiver', foreign_keys='Message.receiver_id')
    notifications = db.relationship('Notification', back_populates='user', foreign_keys='Notification.user_id')
    athlete = db.relationship('Athlete', back_populates='user', uselist=False, foreign_keys='Athlete.user_id')
    coach = db.relationship('Coach', back_populates='user', uselist=False, foreign_keys='Coach.user_id')

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
    position = db.Column(db.String(50), nullable=False)
    achievements = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Defining relationship between the User and Athlete
    user = db.relationship('User', back_populates='athlete')

    def __repr__(self):
        """
        String representation of an Athlete object
        """
        return f'<Athlete {self.user_id}>'


class Coach(db.Model):
    """
    This is for the Coaches, either a Basketball coach
    or a Football coach
    """
    __tablename__ = 'coaches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    coaching_style = db.Column(db.String(100), nullable=False)
    credentials = db.Column(db.Text, nullable=False)
    bio = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Defining the relationship between Coach and User
    user = db.relationship('User', back_populates='coach')

    def __repr__(self):
        """
        String representation of a Coach object
        """
        return f'<Coach {self.user_id}>'


class Message(db.Model):
    """
    Message table in the database for the users to interact.
    i.e Coaches and Athletes.
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Defining relationship with the User table explicitly
    sender = db.relationship('User', back_populates='sent_messages', foreign_keys=[sender_id])
    receiver = db.relationship('User', back_populates='received_messages', foreign_keys=[receiver_id])

    def __repr__(self):
        """
        String representation of the messages from the
        sender to the receiver
        """
        return f'Message sent from {self.sender_id} to {self.receiver_id}'


class Notification(db.Model):
    """
    Notifications table for the messages
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Defining relationship with the User table
    user = db.relationship('User', back_populates='notifications')

    def __repr__(self):
        """
        String rep for notification of messages to
        the users
        """
        return f'Notification {self.message} for User {self.user_id}'
