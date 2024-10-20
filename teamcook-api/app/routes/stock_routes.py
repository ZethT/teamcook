# app/routes/stock_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Stock, Ingredient
from datetime import datetime

stock_bp = Blueprint('stock_bp', __name__, url_prefix='/stocks')

@stock_bp.route('/', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    result = []
    for stock in stocks:
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