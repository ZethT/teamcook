# app/__init__.py

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models and routes
    with app.app_context():
        from app import models, routes

    return app