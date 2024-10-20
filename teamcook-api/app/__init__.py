# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Add this line
from flask_apscheduler import APScheduler
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()  # Add this line
scheduler = APScheduler()

def create_app(config_class=None):
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    app.config.from_object(config_class or 'config.Config')

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate
    scheduler.init_app(app)
    scheduler.start()

    # Import and register blueprints
    from app.routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app