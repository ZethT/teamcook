import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or 'config.Config')

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Import models
        from app import models
        
        # Create tables
        db.create_all()
        
        # Import routes here to avoid circular imports
        from app.routes import user_routes, ingredient_routes, stock_routes, recipe_routes, restaurant_routes, event_routes, stats_routes
        
        # Register blueprints
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(ingredient_routes.ingredient_bp)
        app.register_blueprint(stock_routes.stock_bp)
        app.register_blueprint(recipe_routes.recipe_bp)
        app.register_blueprint(restaurant_routes.restaurant_bp)
        app.register_blueprint(event_routes.event_bp)
        app.register_blueprint(stats_routes.stats_bp)
        
        # Initialize scheduler after all routes are registered
        scheduler.init_app(app)
        scheduler.start()

    return app