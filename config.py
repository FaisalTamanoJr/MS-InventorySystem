""" This module is used for defining configuration settings."""

import os

# The main directory of the application.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # The config variable used by the Flask-WTF extension to protect the app's web forms from CSRF attacks.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'

    # The config variable used by the Flask-SQLAlchemy extension to find the app's database.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
