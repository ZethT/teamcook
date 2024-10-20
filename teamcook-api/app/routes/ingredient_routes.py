# app/routes/ingredient_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Ingredient
from flask_cors import cross_origin


ingredient_bp = Blueprint('ingredient_bp', __name__, url_prefix='/ingredients')

@ingredient_bp.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_ingredients():
    ingredients = Ingredient.query.all()
    result = []
    for ingredient in ingredients:
        ingredient_data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'unit': ingredient.unit,
            'categories': ingredient.categories.split(',') if ingredient.categories else [],
            'type': ingredient.type
        }
        result.append(ingredient_data)
    return jsonify(result), 200

@ingredient_bp.route('/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    ingredient_data = {
        'id': ingredient.id,
        'name': ingredient.name,
        'unit': ingredient.unit,
        'categories': ingredient.categories.split(',') if ingredient.categories else [],
        'type': ingredient.type
    }
    return jsonify(ingredient_data), 200

@ingredient_bp.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_ingredient():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    unit = data.get('unit')
    categories = data.get('categories', '')
    type_ = data.get('type', 'Raw')  # Default to 'Raw'

    if not all([name, unit, type_]):
        return jsonify({'message': 'Missing required fields'}), 400

    if type_ not in ['Raw', 'Processed']:
        return jsonify({'message': "Type must be 'Raw' or 'Processed'"}), 400

    if Ingredient.query.filter_by(name=name).first():
        return jsonify({'message': 'Ingredient with this name already exists'}), 400

    ingredient = Ingredient(
        name=name,
        unit=unit,
        categories=','.join(categories) if isinstance(categories, list) else categories,
        type=type_
    )
    db.session.add(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient created', 'id': ingredient.id}), 201

@ingredient_bp.route('/<int:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', ingredient.name)
    unit = data.get('unit', ingredient.unit)
    categories = data.get('categories', ingredient.categories)
    type_ = data.get('type', ingredient.type)

    if type_ not in ['Raw', 'Processed']:
        return jsonify({'message': "Type must be 'Raw' or 'Processed'"}), 400

    if name != ingredient.name and Ingredient.query.filter_by(name=name).first():
        return jsonify({'message': 'Ingredient with this name already exists'}), 400

    ingredient.name = name
    ingredient.unit = unit
    ingredient.categories = ','.join(categories) if isinstance(categories, list) else categories
    ingredient.type = type_

    db.session.commit()
    return jsonify({'message': 'Ingredient updated'}), 200

@ingredient_bp.route('/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_ingredient(id):
    ingredient = Ingredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'Ingredient deleted'}), 200