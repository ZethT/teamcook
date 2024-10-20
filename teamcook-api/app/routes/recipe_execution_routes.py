# app/routes/recipe_execution_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Recipe, RecipeIngredient, Stock, Ingredient, Sales
from app.utils import allocate_stock
from datetime import datetime, timedelta

recipe_execution_bp = Blueprint('recipe_execution_bp', __name__)

@recipe_execution_bp.route('/execute_processed_recipe', methods=['POST'])
def execute_processed_recipe():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    recipe_id = data.get('recipe_id')
    quantity_to_produce = data.get('quantity')  # Number of units to produce

    if not all([recipe_id, quantity_to_produce]):
        return jsonify({'message': 'Missing required fields'}), 400

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404

    if recipe.type != 'Processed':
        return jsonify({'message': 'Selected recipe is not a processed recipe'}), 400

    # Gather required ingredients
    recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

    allocations = []

    # Allocate ingredients
    for ri in recipe_ingredients:
        total_required = ri.required_amount * quantity_to_produce
        allocated = allocate_stock(ri.ingredient_id, total_required)
        if not allocated:
            return jsonify({'message': f'Insufficient stock for ingredient ID {ri.ingredient_id}'}), 400
        allocations.extend(allocated)

    # Calculate total cost
    total_cost = 0
    for stock, amount in allocations:
        cost_per_unit = stock.cost / (stock.amount + amount) if (stock.amount + amount) > 0 else 0
        total_cost += cost_per_unit * amount

    # Add processing cost if any
    processing_cost = data.get('processing_cost', 0)
    total_cost += processing_cost

    # Check if processed ingredient exists
    processed_ingredient = Ingredient.query.filter_by(name=recipe.name, type='Processed').first()
    if not processed_ingredient:
        # Create processed ingredient
        processed_ingredient = Ingredient(
            name=recipe.name,
            unit=recipe_ingredients[0].unit,  # Assuming unit same as ingredients
            categories='',
            type='Processed'
        )
        db.session.add(processed_ingredient)
        db.session.commit()

    # Create new stock entry for the processed ingredient
    expiry_days = data.get('expiry_days', 60)
    expiry_date = datetime.utcnow() + timedelta(days=expiry_days)

    processed_stock = Stock(
        ingredient_id=processed_ingredient.id,
        name=processed_ingredient.name,
        amount=quantity_to_produce,
        unit=processed_ingredient.unit,
        purchase_date=datetime.utcnow(),
        expiry_date=expiry_date,
        cost=total_cost
    )
    db.session.add(processed_stock)
    db.session.commit()

    return jsonify({'message': 'Processed recipe executed', 'processed_stock_id': processed_stock.id}), 200

@recipe_execution_bp.route('/execute_full_recipe', methods=['POST'])
def execute_full_recipe():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    recipe_id = data.get('recipe_id')
    quantity_to_prepare = data.get('quantity')  # Number of units to prepare
    sale_price = data.get('sale_price')

    if not all([recipe_id, quantity_to_prepare, sale_price]):
        return jsonify({'message': 'Missing required fields'}), 400

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404

    if recipe.type != 'Full Recipe':
        return jsonify({'message': 'Selected recipe is not a full recipe'}), 400

    # Gather required ingredients
    recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

    allocations = []

    # Allocate ingredients
    for ri in recipe_ingredients:
        total_required = ri.required_amount * quantity_to_prepare
        allocated = allocate_stock(ri.ingredient_id, total_required)
        if not allocated:
            return jsonify({'message': f'Insufficient stock for ingredient ID {ri.ingredient_id}'}), 400
        allocations.extend(allocated)

    # Record the sale
    sale = Sales(
        recipe_id=recipe_id,
        quantity=quantity_to_prepare,
        sale_price=sale_price,
        restaurant_id=recipe.restaurant_id
    )
    db.session.add(sale)
    db.session.commit()

    return jsonify({'message': f'Full recipe executed and {quantity_to_prepare} units sold'}), 200