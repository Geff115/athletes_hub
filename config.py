#!/usr/bin/env python3
"""
This script configures the various parts of our
application such as development, testing, and
production.
"""


import os
import logging
import json
import requests
import secrets
from datadog import initialize, api
from datadog import DogStatsd
from urllib.parse import quote_plus


DB_USER = os.getenv('ATHLETES_HUB_DB_USER', 'athlete')
DB_PWD = quote_plus(os.getenv('ATHLETES_HUB_DB_PWD', 'Sport@123'))
DB_HOST = os.getenv('ATHLETES_HUB_DB_HOST', 'localhost')
DB_PORT = os.getenv('ATHLETES_HUB_DB_PORT', '3306')

class BaseConfig:
    """
    The Base class with common settings that applies
    to all environments.
    """
    SECRET_KEY_FLASK = secrets.token_urlsafe(50)

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/athletes_hub_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """
    Inheriting from BaseConfig class and add or override
    settings specific to the development environment
    """
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_app(app):
        """setting up logging"""
        logging.basicConfig(level=DevelopmentConfig.LOGGING_LEVEL, format=DevelopmentConfig.LOGGING_FORMAT)


class TestingConfig(BaseConfig):
    """
    Inheriting from BaseConfig class. Using an in-memory SQLite
    database, ensuring that testing frameworks can operate
    without interference.
    """
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    LOGGING_LEVEL = logging.WARNING


class DatadogLogHandler(logging.Handler):
    """
    Custom logging handler to send logs to Datadog
    """
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('DATADOG_API_KEY')
        self.endpoint = f'https://http-intake.logs.datadoghq.com/v1/input/{self.api_key}'
        self.headers = {
                'Content-Type': 'application/json',
                'DD-API-KEY': self.api_key
        }

    def emit(self, record):
        try:
            log_entry = self.format(record)
            payload = {
                    'message': log_entry,
                    'ddsource': 'flask',
                    'service': 'athletes_hub_app',
                    'hostname': os.getenv('HOSTNAME', 'unknown')
            }
            response = requests.post(self.endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
        except Exception as e:
            self.handleError(record)


class ProductionConfig(BaseConfig):
    """
    Ensuring the application runs safely and efficiently in a
    production environment.
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY_FLASK')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/athletes_hub_db"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_SSL_REDIRECT = True

    @staticmethod
    def init_app(app):
        """A login handler that sends logs to Datadog using
        the Datadog library.
        """
        handler = DatadogLogHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
}
