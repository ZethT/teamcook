# app/routes.py

from flask import request, jsonify, current_app
from app import db
from app.models import Stock, Quantity, RawIngredient
from datetime import datetime

# Access the app instance
app = current_app

@app.route('/stocks', methods=['GET'])
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
            'quantity': {
                'amount': stock.quantity.amount,
                'unit': stock.quantity.unit
            },
            'raw_ingredient_id': stock.raw_ingredient_id
        }
        result.append(stock_data)
    return jsonify(result), 200

@app.route('/stocks/<int:id>', methods=['GET'])
def get_stock(id):
    stock = Stock.query.get_or_404(id)
    stock_data = {
        'id': stock.id,
        'name': stock.name,
        'purchase_date': stock.purchase_date.isoformat(),
        'expiry_date': stock.expiry_date.isoformat(),
        'cost': stock.cost,
        'quantity': {
            'amount': stock.quantity.amount,
            'unit': stock.quantity.unit
        },
        'raw_ingredient_id': stock.raw_ingredient_id
    }
    return jsonify(stock_data), 200

@app.route('/stocks', methods=['POST'])
def create_stock():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and extract data
    name = data.get('name')
    purchase_date = data.get('purchase_date')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost')
    quantity_data = data.get('quantity')
    raw_ingredient_id = data.get('raw_ingredient_id')

    if not all([name, expiry_date, cost, quantity_data, raw_ingredient_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    quantity = Quantity(amount=quantity_data['amount'], unit=quantity_data['unit'])
    db.session.add(quantity)
    db.session.commit()

    stock = Stock(
        name=name,
        purchase_date=datetime.fromisoformat(purchase_date) if purchase_date else datetime.utcnow(),
        expiry_date=datetime.fromisoformat(expiry_date),
        cost=cost,
        quantity=quantity,
        raw_ingredient_id=raw_ingredient_id
    )
    db.session.add(stock)
    db.session.commit()
    return jsonify({'message': 'Stock created', 'id': stock.id}), 201

@app.route('/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    stock = Stock.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    stock.name = data.get('name', stock.name)
    stock.purchase_date = datetime.fromisoformat(data.get('purchase_date')) if data.get('purchase_date') else stock.purchase_date
    stock.expiry_date = datetime.fromisoformat(data.get('expiry_date')) if data.get('expiry_date') else stock.expiry_date
    stock.cost = data.get('cost', stock.cost)

    quantity_data = data.get('quantity')
    if quantity_data:
        stock.quantity.amount = quantity_data.get('amount', stock.quantity.amount)
        stock.quantity.unit = quantity_data.get('unit', stock.quantity.unit)

    stock.raw_ingredient_id = data.get('raw_ingredient_id', stock.raw_ingredient_id)

    db.session.commit()
    return jsonify({'message': 'Stock updated'}), 200

@app.route('/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return jsonify({'message': 'Stock deleted'}), 200
