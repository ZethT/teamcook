# app/routes/restaurant_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Restaurant

restaurant_bp = Blueprint('restaurant_bp', __name__, url_prefix='/restaurants')

@restaurant_bp.route('/', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    result = []
    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'phone': restaurant.phone
        }
        result.append(restaurant_data)
    return jsonify(result), 200

@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'phone': restaurant.phone
    }
    return jsonify(restaurant_data), 200

@restaurant_bp.route('/', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    address = data.get('address', '')
    phone = data.get('phone', '')

    if not name:
        return jsonify({'message': 'Missing required fields'}), 400

    if Restaurant.query.filter_by(name=name).first():
        return jsonify({'message': 'Restaurant with this name already exists'}), 400

    restaurant = Restaurant(
        name=name,
        address=address,
        phone=phone
    )
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant created', 'id': restaurant.id}), 201

@restaurant_bp.route('/<int:id>', methods=['PUT'])
def update_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', restaurant.name)
    address = data.get('address', restaurant.address)
    phone = data.get('phone', restaurant.phone)

    if name != restaurant.name and Restaurant.query.filter_by(name=name).first():
        return jsonify({'message': 'Restaurant with this name already exists'}), 400

    restaurant.name = name
    restaurant.address = address
    restaurant.phone = phone

    db.session.commit()
    return jsonify({'message': 'Restaurant updated'}), 200

@restaurant_bp.route('/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant deleted'}), 200