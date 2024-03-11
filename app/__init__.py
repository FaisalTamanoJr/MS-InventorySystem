"""This file defines what symbols are made available outside and also creates the app package."""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask instance. The "__name__" argument is used by Flask as a starting point for loading resource.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # Database instance represented in the app.

# The migration engine used to allow the app to migrate (in case the app's database needs to change or grow).
migrate = Migrate(app, db)

from app import routes, models  # Although it seems odd, the import was placed here to deal with the circular import issue.
