"""This file defines what symbols are made available outside and also creates the app package."""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Flask instance. The "__name__" argument is used by Flask as a starting point for loading resource.
db = SQLAlchemy()  # Database instance represented in the app.

# The migration engine used to allow the app to migrate (in case the app's database needs to change or grow).
migrate = Migrate()

# The flask login extension that allows users to remain signed it after they have logged in.
login = LoginManager()
login.login_view = 'main.login' # Assigns the login page that gets redirected to when a view function is under
# @login_required.

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import helpers, models  # Although it seems odd, the import was placed here to deal with the circular import
# issue.
