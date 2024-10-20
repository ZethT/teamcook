# app/__init__.py

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
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type", "Authorization"]}})
    app.config.from_object(config_class or 'config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)
    scheduler.start()

    # Import and register blueprints
    from app.routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response
    
    return app