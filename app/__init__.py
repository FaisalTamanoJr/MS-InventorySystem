"""This file defines what symbols are made available outside and also creates the app package."""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Flask instance. The "__name__" argument is used by Flask as a starting point for loading resource.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # Database instance represented in the app.

# The migration engine used to allow the app to migrate (in case the app's database needs to change or grow).
migrate = Migrate(app, db)

# The flask login extension that allows users to remain signed it after they have logged in
login = LoginManager(app)

from app import routes, models  # Although it seems odd, the import was placed here to deal with the circular import issue.
