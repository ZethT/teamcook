# app/routes/__init__.py

from app.routes.stock_routes import stock_bp
from app.routes.ingredient_routes import ingredient_bp
from app.routes.user_routes import user_bp
from app.routes.restaurant_routes import restaurant_bp
from app.routes.recipe_routes import recipe_bp
from app.routes.recipe_execution_routes import recipe_execution_bp
from app.routes.event_routes import event_bp
from app.routes.waste_routes import waste_bp
from app.routes.stats_routes import stats_bp

blueprints = [
    stock_bp,
    ingredient_bp,
    user_bp,
    restaurant_bp,
    recipe_bp,
    recipe_execution_bp,
    event_bp,
    waste_bp,
    stats_bp
]