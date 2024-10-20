# app/routes/stock_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Stock, Ingredient, Waste, Sales, Recipe, Event, RecipeIngredient
from datetime import datetime
from sqlalchemy import func, desc

stock_bp = Blueprint('stock_bp', __name__, url_prefix='/stocks')

@stock_bp.route('/', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    result = []
    for stock in stocks:
        ingredient = Ingredient.query.get(stock.ingredient_id)
        stock_data = {
            'id': stock.id,
            'name': stock.name,
            'purchase_date': stock.purchase_date.isoformat(),
            'expiry_date': stock.expiry_date.isoformat(),
            'cost': stock.cost,
            'amount': stock.amount,
            'unit': stock.unit,
            'ingredient_id': stock.ingredient_id,
            'ingredient_name': ingredient.name  # Add ingredient_name
        }
        result.append(stock_data)
    return jsonify(result), 200

@stock_bp.route('/<int:id>', methods=['GET'])
def get_stock(id):
    stock = Stock.query.get_or_404(id)
    stock_data = {
        'id': stock.id,
        'name': stock.name,
        'purchase_date': stock.purchase_date.isoformat(),
        'expiry_date': stock.expiry_date.isoformat(),
        'cost': stock.cost,
        'amount': stock.amount,
        'unit': stock.unit,
        'ingredient_id': stock.ingredient_id
    }
    return jsonify(stock_data), 200

@stock_bp.route('/', methods=['POST'])
def create_stock():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and extract data
    name = data.get('name')
    purchase_date = data.get('purchase_date')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost')
    amount = data.get('amount')
    unit = data.get('unit')
    ingredient_id = data.get('ingredient_id')

    # Check for missing required fields
    missing_fields = []
    if name is None or name == '':
        missing_fields.append('name')
    if expiry_date is None or expiry_date == '':
        missing_fields.append('expiry_date')
    if cost is None:
        missing_fields.append('cost')
    if amount is None:
        missing_fields.append('amount')
    if unit is None or unit == '':
        missing_fields.append('unit')
    if ingredient_id is None:
        missing_fields.append('ingredient_id')

    if missing_fields:
        return jsonify({'message': 'Missing required fields', 'fields': missing_fields}), 400

    # Check if Ingredient exists
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        return jsonify({'message': 'Ingredient not found'}), 404

    # Parse dates
    try:
        purchase_date = datetime.fromisoformat(purchase_date) if purchase_date else datetime.utcnow()
        expiry_date = datetime.fromisoformat(expiry_date)
    except ValueError as e:
        return jsonify({'message': 'Invalid date format', 'error': str(e)}), 400

    # Create stock instance
    stock = Stock(
        name=name,
        purchase_date=purchase_date,
        expiry_date=expiry_date,
        cost=float(cost),
        amount=float(amount),
        unit=unit,
        ingredient_id=ingredient_id
    )
    db.session.add(stock)
    db.session.commit()
    return jsonify({'message': 'Stock created', 'id': stock.id}), 201

@stock_bp.route('/<int:id>', methods=['PUT'])
def update_stock(id):
    stock = Stock.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', stock.name)
    purchase_date = data.get('purchase_date')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost', stock.cost)
    amount = data.get('amount', stock.amount)
    unit = data.get('unit', stock.unit)
    ingredient_id = data.get('ingredient_id', stock.ingredient_id)

    if ingredient_id != stock.ingredient_id:
        # If ingredient_id is being updated, check if the new Ingredient exists
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({'message': 'Ingredient not found'}), 404
        stock.ingredient_id = ingredient_id

    stock.name = name
    stock.purchase_date = datetime.fromisoformat(purchase_date) if purchase_date else stock.purchase_date
    stock.expiry_date = datetime.fromisoformat(expiry_date) if expiry_date else stock.expiry_date
    stock.cost = cost
    stock.amount = amount
    stock.unit = unit

    db.session.commit()
    return jsonify({'message': 'Stock updated'}), 200

@stock_bp.route('/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return jsonify({'message': 'Stock deleted'}), 200



@stock_bp.route('/grouped', methods=['GET'])
def get_grouped_stocks():
    try:
        # Perform a join between Stock and Ingredient to get ingredient details
        grouped_stocks = (
            db.session.query(
                Ingredient.id.label('ingredient_id'),
                Ingredient.name.label('ingredient_name'),
                func.sum(Stock.amount).label('total_amount'),
                Stock.unit.label('unit')  # Assuming unit is consistent per ingredient
            )
            .join(Ingredient, Stock.ingredient_id == Ingredient.id)
            .group_by(Ingredient.id, Ingredient.name, Stock.unit)
            .all()
        )

        # Convert the result to a list of dictionaries
        result = []
        for stock in grouped_stocks:
            result.append({
                'ingredient_id': stock.ingredient_id,
                'ingredient_name': stock.ingredient_name,
                'total_amount': stock.total_amount,
                'unit': stock.unit
            })

        return jsonify(result), 200

    except Exception as e:
        # Log the exception if you have a logging system
        print(f"Error in get_grouped_stocks: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    

@stock_bp.route('/log/<string:ingredient_name>', methods=['GET'])
def get_stock_log(ingredient_name):
    try:
        # Get the ingredient
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first_or_404()

        # Fetch stock creations
        stock_creations = (
            Stock.query
            .filter_by(ingredient_id=ingredient.id)
            .order_by(desc(Stock.purchase_date))
            .all()
        )

        # Fetch processed recipe executions (consumptions)
        processed_executions = (
            Event.query
            .filter(Event.name.like(f"Processed Recipe:%"))
            .order_by(desc(Event.time))
            .all()
        )

        # Fetch full recipe executions (consumptions)
        full_executions = (
            Sales.query
            .join(Recipe, Sales.recipe_id == Recipe.id)
            .join(RecipeIngredient, RecipeIngredient.recipe_id == Recipe.id)
            .filter(RecipeIngredient.ingredient_id == ingredient.id)
            .order_by(desc(Sales.sale_date))
            .all()
        )

        # Fetch waste entries
        wastes = (
            Waste.query
            .join(Stock, Waste.stock_id == Stock.id)
            .filter(Stock.ingredient_id == ingredient.id)
            .order_by(desc(Waste.waste_date))
            .all()
        )

        # Combine and sort all entries
        log_entries = []

        for creation in stock_creations:
            log_entries.append({
                'type': 'Stock Added',
                'date': creation.purchase_date.isoformat(),
                'amount': creation.amount,
                'unit': creation.unit
            })

        for execution in processed_executions:
            # Parse the event name to get recipe details
            _, recipe_name, amount, unit = execution.name.split(':')
            if ingredient_name in recipe_name:
                log_entries.append({
                    'type': 'Consumed (Processed Recipe)',
                    'date': execution.time.isoformat(),
                    'amount': float(amount),
                    'unit': unit.strip(),
                    'details': f"Used in {recipe_name.strip()}"
                })

        for sale in full_executions:
            recipe_ingredient = RecipeIngredient.query.filter_by(recipe_id=sale.recipe_id, ingredient_id=ingredient.id).first()
            if recipe_ingredient:
                consumed_amount = recipe_ingredient.required_amount * sale.quantity
                log_entries.append({
                    'type': 'Consumed (Full Recipe)',
                    'date': sale.sale_date.isoformat(),
                    'amount': consumed_amount,
                    'unit': recipe_ingredient.unit,
                    'details': f"Used in {sale.recipe.name}"
                })

        for waste in wastes:
            log_entries.append({
                'type': 'Expired/Wasted',
                'date': waste.waste_date.isoformat(),
                'amount': waste.waste_amount,
                'unit': waste.unit,
                'reason': waste.reason
            })

        # Sort all entries by date, most recent first
        log_entries.sort(key=lambda x: x['date'], reverse=True)

        return jsonify(log_entries), 200

    except Exception as e:
        print(f"Error in get_stock_log: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500