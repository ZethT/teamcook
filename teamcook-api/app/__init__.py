import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()

def create_app(config_class=None):
    app = Flask(__name__)

    # Load configuration
    config_name = config_class or os.getenv('FLASK_CONFIG', 'config.Config')
    app.config.from_object(config_name)

    # Set up logging
    setup_logging(app)

    # Configure CORS
    configure_cors(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)

    with app.app_context():
        # Import models
        from app import models

        # Create tables
        db.create_all()

        # Import and register blueprints
        register_blueprints(app)

        # Start the scheduler
        scheduler.start()

    return app

def setup_logging(app):
    """Configure logging for the Flask application."""
    # Create a file handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Define log format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to the app's logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

def configure_cors(app):
    """Configure CORS to allow requests from the frontend."""
    # Allow both 'localhost' and '127.0.0.1' to handle different access methods
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"]
        }
    }, supports_credentials=True)

def register_blueprints(app):
    """Import and register all blueprints."""
    from app.routes import (
        user_routes,
        ingredient_routes,
        stock_routes,
        recipe_routes,
        restaurant_routes,
        event_routes,
        stats_routes,
        recipe_execution_routes
    )

    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(ingredient_routes.ingredient_bp)
    app.register_blueprint(stock_routes.stock_bp)
    app.register_blueprint(recipe_routes.recipe_bp)
    app.register_blueprint(restaurant_routes.restaurant_bp)
    app.register_blueprint(event_routes.event_bp)
    app.register_blueprint(stats_routes.stats_bp)
    app.register_blueprint(recipe_execution_routes.recipe_execution_bp)