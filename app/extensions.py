"""
Central place for Flask extension instances.

These are created here (unbound) and initialized inside the application
factory with app.init_app(). Keeping them here avoids circular imports
between app/__init__.py, models, and routes.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Where Flask-Login redirects unauthenticated users
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"