#!/usr/bin/env python3
"""
Setting up the database models for
athletes_hub_db using SQLAlchemy ORM
"""


from .extensions import db
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
    last_name = db.Column(db.string(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sport = db.Column(db.string(50), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True)

    # Defining relationships between models
    messages = db.relationship('Message', backref='user', lazy=True)
    notification = db.relationship('Notification', backref='user', lazy=True)
    athlete = db.relationship('Athlete', backref='user', uselist=False)
    coach = db.relationship('Coach', backref='user', uselist=False)

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

    id = db.Column(db.Integerx, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, default=datetime.utcnow)

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

    def __repr__(self):
        """
        String rep for notification of messages to
        the users
        """
        return f'Notification {self.message} for User {self.user_id}'
